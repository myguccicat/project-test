# modules/sentiment.py
from snownlp import SnowNLP
from collections import Counter

def classify_sentiment(text):
    s = SnowNLP(text)
    score = s.sentiments
    if score > 0.66:
        label = "正向"
    elif score < 0.33:
        label = "負向"
    else:
        label = "中立"
    return label, score

def analyze_sentiments(texts):
    labels = []
    scores = []

    for text in texts:
        label, score = classify_sentiment(text)
        labels.append(label)
        scores.append(score)

    counts = dict(Counter(labels))
    average = sum(scores) / len(scores) if scores else 0.0

    return {
        "counts": counts,
        "average": average
    }
