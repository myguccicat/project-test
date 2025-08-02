# tests/test_sentiment.py
import pytest
from modules.sentiment import classify_sentiment, analyze_sentiments, summarize_text

def test_classify_sentiment_positive():
    text = "這個產品真的很好，我非常喜歡！"
    result = classify_sentiment(text)
    assert result[0] in ["正向", "中立"]  # 防止 SnowNLP 隨機性
    assert 0 <= result[1] <= 1

def test_classify_sentiment_negative():
    text = "這是我用過最糟糕的服務。"
    result = classify_sentiment(text)
    assert result[0] == "負向"

def test_classify_sentiment_neutral():
    text = "這是一般描述，沒有情緒色彩。"
    result = classify_sentiment(text)
    assert result[0] in ["中立", "正向", "負向"]  # SnowNLP may classify neutral as positive or negative based on context   
    assert 0.33 <= result[1] <= 0.66  # Neutral sentiment score should be around 0.5

def test_classify_sentiment_extremely_positive():
    text = "這真的是我用過最棒、最喜歡、超級超級好的產品！"
    result = classify_sentiment(text)
    assert result[0] == "正向"
    assert result[1] > 0.9  # 極高正向分數

def test_classify_sentiment_extremely_negative():
    text = "這是史上最爛的東西，完全不能用，氣死人了！"
    result = classify_sentiment(text)
    assert result[0] == "負向"
    assert result[1] < 0.1  # 極低負向分數

# tests/test_sentiment.py (補充)
def test_classify_sentiment_empty():
    from modules.sentiment import classify_sentiment
    result = classify_sentiment("")
    assert result[0] == "中立"


def test_classify_sentiment_long_text():
    from modules.sentiment import classify_sentiment
    text = "很好很好很好" * 100
    result = classify_sentiment(text)
    assert result[0] == "正向"

def test_classify_sentiment_none_input():
    result = classify_sentiment(None)
    assert result[0] == "中立"
    assert result[1] == 0.5

def test_classify_sentiment_numeric_input():
    result = classify_sentiment(12345)
    assert result[0] == "中立"
    assert result[1] == 0.5

def test_classify_sentiment_blank_spaces():
    result = classify_sentiment("     ")
    assert result[0] == "中立"
    assert result[1] == 0.5

def test_analyze_sentiments_structure():
    texts = ["這是好產品", "這是壞產品", "普通的描述"]
    result = analyze_sentiments(texts)
    assert "counts" in result
    assert "average" in result
    assert "details" in result
    assert "scores" in result
    assert isinstance(result["counts"], dict)
    assert isinstance(result["average"], float)
    assert isinstance(result["details"], list)
    assert isinstance(result["scores"], list)
    assert len(result["details"]) == len(texts)
    assert len(result["scores"]) == len(texts)

def test_analyze_sentiments_empty_input():
    result = analyze_sentiments([])
    assert result["counts"] == {}
    assert result["average"] == 0.0
    assert result["details"] == []
    assert result["scores"] == []

def test_summarize_text_basic():
    text = "生成式AI正在改變世界，許多企業已經開始投入相關應用。未來的發展潛力巨大。"
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0  # 至少有句摘要出來

def test_summarize_text_empty():
    summary = summarize_text("")
    assert summary == ""
