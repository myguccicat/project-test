# import pytest
# from modules.topic_model import extract_topics

# def test_extract_topics_simple_case():
#     topics = extract_topics(["這是一則新聞", "另一則關於經濟的新聞"])
#     assert isinstance(topics, list)
#     assert len(topics) > 0

# tests/test_topic_model.py
import pytest
from modules.topic_model import extract_topics

def test_extract_topics_structure():
    texts = ["AI 正在改變世界", "資安議題愈來愈重要"]
    result = extract_topics(texts)
    assert isinstance(result, list)
    for topic in result:
        assert "cluster" in topic
        assert "keywords" in topic
        assert "article_idxs" in topic
