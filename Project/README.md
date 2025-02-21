# Final project(Persian tweets): Pixie+Spam Detection+Stream Analysis

Some of tasks done in this project:
- Using the Pixie algorithm,create a graph of users and their interactions.
<div style="text-align: center;">
    <img src="1.png" alt="Alt Text" width="300">
</div>

```markdown
Pixie Similarity Results (based on random walks starting from 'Armanjasoor'):
User: adam_hesabi, Visits: 19
Pixie Similarity Results (based on random walks starting from 'Armanjasoor'):
User: Ivar_lathbrug2, Visits: 15
Pixie Similarity Results (based on random walks starting from 'Armanjasoor'):
User: _Mahdiyar313, Visits: 14
Pixie Similarity Results (based on random walks starting from 'Armanjasoor'):
...
```
- Using the TrustRank algorithm and calculating Spam Mass, design and implement an algorithm that can detect spam tweets.
```markdown
+--------------------+------------------+
|                text|        spam_value|
+--------------------+------------------+
|دوستانی که ریموت ...|2.3017633100286403|
|به عنوان پزشک، دا...| 6.385299525535547|
|بنا به نظر #وزیر_...|11920.432214382174|
|ظاهراً سازمان اطل...| 3126.438134169463|
|اگر صحبت‌های آ.عج...|  797.080963052442|
...
```
- Using PySpark's Structured Streaming, process new tweets in real-time and identify and count the hashtags of each tweet.
```markdown
+--------------------+--------------------+-------------+
|              window|             hashtag|hashtag_count|
+--------------------+--------------------+-------------+
|{2023-12-01 06:14...|         پرستو_معینی|            1|
|{2023-11-22 11:18...|        دلیران_میدان|            1|
|{2023-12-01 06:14...|          زهرا_صفایی|            1|
|{2023-11-10 07:10...|         درمان_سرطان|            1|
|{2023-11-10 07:10...|       سرطان_پروستات|            1|
...
```
- Use the sentiment feature of each tweet to analyze sentiment and calculate and display the average sentiment for each hashtag in real-time.
```markdown
+--------------------+-------------+
|             hashtag|avg_sentiment|
+--------------------+-------------+
|          حسن_روحانی|          0.0|
|         قیام_سراسری|          0.0|
|                 یمن|          0.0|
|       آرمیتا_گراوند|          0.0|
|    KingRezaPahlavi‌|          0.0|
...
```
