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
    details = []  # 每篇文章的情緒細節
    labels = []
    scores = []

    for text in texts:
        label, score = classify_sentiment(text)
        labels.append(label)
        scores.append(score)
        details.append({
            "title": text,
            "label": label,
            "score": score
        })

    counts = dict(Counter(labels))
    average = sum(scores) / len(scores) if scores else 0.0

    return {
        "counts": counts,
        "average": average,
        "details": details,  # 新增每篇文章細節
        "scores": scores      # 純數字分數 array (for 圖表用)
    }

def summarize_text(text, max_sentences=2):
    s = SnowNLP(text)
    summary = s.summary(max_sentences)
    return ' '.join(summary)
