import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def extract_topics(texts, n_clusters=3, top_k=5):
    # --- 1. 中文斷詞 ---
    tokenized_texts = [' '.join(jieba.cut(text)) for text in texts]

    # --- 2. TF-IDF 向量化 ---
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(tokenized_texts)

    # --- 3. 動態調整群數 ---
    n_clusters = min(n_clusters, X.shape[0])

    # --- 4. KMeans 分群 ---
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    # --- 5. 每群挑 top K 關鍵字 ---
    keywords = []
    for cluster in np.unique(labels):
        idxs = np.where(labels == cluster)[0]
        centroid = X[idxs].mean(axis=0)
        sorted_idx = np.asarray(centroid).flatten().argsort()[::-1]
        top_terms = [vectorizer.get_feature_names_out()[i] for i in sorted_idx[:top_k]]
        keywords.append({
            "cluster": int(cluster),
            "keywords": top_terms,
            "article_idxs": idxs.tolist()  # <--- 這行是重點
        })

    return keywords
