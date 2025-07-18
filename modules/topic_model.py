# modules/topic_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text
import plotly.graph_objects as go
import numpy as np
import jieba
from collections import Counter

def join_tokens(docs):
    return [" ".join(tokens) for tokens in docs]

def extract_top_keywords_per_cluster(X, labels, vectorizer, top_n=3):
    keywords = []
    for cluster in np.unique(labels):
        idxs = np.where(labels == cluster)[0]
        centroid = X[idxs].mean(axis=0)
        sorted_idx = np.asarray(centroid.todense()).flatten().argsort()[::-1]
        feature_names = np.array(vectorizer.get_feature_names_out())
        top_keywords = feature_names[sorted_idx[:top_n]]
        keywords.append("主題「{}」".format("、".join(top_keywords)))
    return keywords

def generate_topics(cleaned_texts, n_clusters=5):
    texts = join_tokens(cleaned_texts)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X)
    labels = kmeans.labels_

    topic_names = extract_top_keywords_per_cluster(X, labels, vectorizer)
    topic_counts = Counter(labels)

    topic_labels = [topic_names[i] for i in range(n_clusters)]
    topic_values = [topic_counts[i] for i in range(n_clusters)]

    fig = go.Figure(go.Bar(x=topic_labels, y=topic_values))
    fig.update_layout(title="主題分布", xaxis_title="主題", yaxis_title="文章數")

    return topic_labels, fig
