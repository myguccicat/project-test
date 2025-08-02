# modules/nlp.py
import jieba
import re

STOPWORDS = set(["的", "了", "是", "在", "和", "也", "有", "與", "及", "為", "不", "就"])

def clean_text(text):
    text = re.sub(r"[\s\d\W_]+", "", text)  # 移除符號與數字
    return text

def clean_and_tokenize(texts):
    tokenized = []
    for t in texts:
        t = clean_text(t)
        tokens = [w for w in jieba.cut(t) if w not in STOPWORDS and len(w) > 1]
        tokenized.append(tokens)
    return tokenized

def tokenize(text):
    """
    將單一文字斷詞並過濾停用詞。
    """
    text = clean_text(text)
    return [w for w in jieba.cut(text) if w not in STOPWORDS and len(w) > 1]

def generate_ngrams(tokens, n=2):
    """
    生成 n-gram。
    """
    return ["".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

