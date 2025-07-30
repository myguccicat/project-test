import pytest
from modules.topic_model import extract_topics

def test_extract_topics_simple_case():
    topics = extract_topics(["這是一則新聞", "另一則關於經濟的新聞"])
    assert isinstance(topics, list)
    assert len(topics) > 0
