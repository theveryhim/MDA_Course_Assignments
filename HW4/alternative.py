import time
import pandas as pd
from pyspark.sql import SparkSession as ss
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType
import matplotlib.pyplot as plt

# Initialize Spark session
spark = ss.builder.appName("MDA2024-HW4").master("local[*]").config("spark.executor.memory", "2g")\
    .config("spark.driver.memory", "2g").config("spark.hadoop.native.lib", "false")\
    .config("spark.sql.files.ignoreCorruptFiles", "true") \
    .config("spark.sql.files.ignoreMissingFiles", "true") \
    .config("spark.hadoop.io.nativeio.NativeIO", "false") \
    .getOrCreate()

input_file = "C:/Users/HAMAHANG/Desktop/sut/S7/MDA/HW/4/Datasets/web_streaming_dataset.csv"
stream_file = "C:/Users/HAMAHANG/Desktop/sut/S7/MDA/HW/4/Datasets/streaming_data.txt"

# Read the dataset
df = pd.read_csv(input_file)
request_types = df['RequestType'].tolist()

# Write the dataset bit by bit to a new file
with open(stream_file, 'w') as f:
    for bit in request_types:
        f.write(f"{bit}\n")

# Define the schema for the streaming data
schema = StructType([StructField("RequestType", IntegerType(), True)])

# Read the stream from the file
stream_df = spark.readStream.schema(schema).option("maxFilesPerTrigger", 1).csv(stream_file)

# Convert the stream to a DStream
stream_query = stream_df.writeStream.format("memory").queryName("stream").start()

# Wait for the stream to start and collect all data
time.sleep(5)  # Allow time for the stream to start
stream_data = spark.sql("SELECT * FROM stream").collect()
stream_bits = [row['RequestType'] for row in stream_data]

# Stop the stream
stream_query.stop()

# DGIM Algorithm Implementation
class DGIM:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buckets = []
        self.timestamp = 0

    def update(self, bit):
        self.timestamp += 1
        if bit == 1:
            self.buckets.append((self.timestamp, 1))
            self.merge()

        # Remove old buckets
        while self.buckets and self.buckets[0][0] <= self.timestamp - self.window_size:
            self.buckets.pop(0)

    def merge(self):
        i = len(self.buckets) - 1
        while i >= 1:
            if self.buckets[i][1] == self.buckets[i-1][1]:
                self.buckets[i-1] = (self.buckets[i-1][0], self.buckets[i-1][1] + self.buckets[i][1])
                self.buckets.pop(i)
            i -= 1

    def estimate(self):
        count = 0
        for bucket in self.buckets:
            count += bucket[1]
        return count

# Initialize DGIM with window size 500
dgim = DGIM(500)

# Process the stream data in windows of 500 bits
window_size = 500
num_windows = 15
actual_counts = []
estimated_counts = []

for i in range(num_windows):
    # Get the current window data
    start_index = i
    end_index = start_index + window_size
    window_bits = stream_bits[start_index:end_index]

    # Update DGIM with the new bits
    for bit in window_bits:
        dgim.update(bit)

    # Calculate actual and estimated counts
    actual_count = sum(window_bits)
    estimated_count = dgim.estimate()

    # Append to lists
    actual_counts.append(actual_count)
    estimated_counts.append(estimated_count)

    # Print the results
    print(f"Window {i+1}: Actual Count = {actual_count}, Estimated Count = {estimated_count}")

# Plot the results
plt.plot(range(1, num_windows + 1), actual_counts, label='Actual Count')
plt.plot(range(1, num_windows + 1), estimated_counts, label='Estimated Count')
plt.xlabel('Window')
plt.ylabel('Count')
plt.legend()
plt.show()