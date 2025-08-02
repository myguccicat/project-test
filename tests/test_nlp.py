import pytest
from modules.nlp import tokenize, generate_ngrams, clean_and_tokenize

def test_tokenize():
    text = "生成式AI正在改變世界。"
    tokens = tokenize(text)
    assert isinstance(tokens, list)
    assert all(isinstance(t, str) for t in tokens)
    assert "生成式" in tokens or "改變" in tokens

def test_generate_ngrams():
    tokens = ["生成式", "AI", "改變", "世界"]
    bigrams = generate_ngrams(tokens, n=2)
    assert bigrams == ["生成式AI", "AI改變", "改變世界"]

    trigrams = generate_ngrams(tokens, n=3)
    assert trigrams == ["生成式AI改變", "AI改變世界"]

def test_clean_and_tokenize():
    texts = ["這是第一篇文章。", "生成式AI的應用很廣泛。"]
    tokenized = clean_and_tokenize(texts)
    assert isinstance(tokenized, list)
    assert all(isinstance(t, list) for t in tokenized)
    assert any("生成式" in t for t in tokenized)
