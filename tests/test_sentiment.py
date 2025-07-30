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
    text = "這只是一個普通的產品介紹。"
    result = classify_sentiment(text)
    assert result[0] == "中立"
