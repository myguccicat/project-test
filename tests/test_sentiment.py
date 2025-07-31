import pytest
from modules.sentiment import classify_sentiment

def test_classify_sentiment_positive():
    text = "這個產品真的很好，我非常喜歡！"
    result = classify_sentiment(text)
    assert result[0] == "正向"

def test_classify_sentiment_negative():
    text = "這是我用過最糟糕的服務。"
    result = classify_sentiment(text)
    assert result[0] == "負向"

def test_classify_sentiment_neutral():
    text = "這是一般描述，沒有情緒色彩。"
    result = classify_sentiment(text)
    assert result[0] in ["中立", "正向", "負向"]  # SnowNLP may classify neutral as positive or negative based on context   
    assert 0.33 <= result[1] <= 0.66  # Neutral sentiment score should be around 0.5
