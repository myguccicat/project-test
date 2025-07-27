# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
from collections import Counter
import itertools

# --- Load API Key from .env ---
load_dotenv()

# --- Other imports ---
from modules.crawler import fetch_articles
from modules.nlp import clean_text
from modules.topic_model import extract_topics
from sklearn.feature_extraction.text import CountVectorizer
from modules.sentiment import analyze_sentiments
from modules.suggestion import generate_business_suggestions
from modules.utils import log_app_usage  # <--- 新增
from cache.cache_utils import load_cache, save_cache

# --- Streamlit App Logic ---
st.set_page_config(page_title="趨勢分析與商業建議", layout="wide")
st.title("🔍 關鍵字趨勢分析與商業建議工具")

keyword = st.text_input("請輸入關鍵字:")
mode = st.selectbox("選擇資料來源:", ["ptt", "news"])
vectorizer = CountVectorizer()

if st.button("執行分析") and keyword:
    log_app_usage(f"[App] User Input Keyword: {keyword} ({mode})")  # <--- 記錄輸入

    cache_data = load_cache(keyword, mode)

    if cache_data:
        st.info("使用快取資料 (1 小時內最新)")
        articles = cache_data
        log_app_usage(f"[App] Cache Hit: {keyword} ({mode})")  # <--- 記錄快取命中
    else:
        api_key = os.getenv("NEWS_API_KEY")
        articles = fetch_articles(keyword, mode=mode, limit=10, api_key=api_key)
        if articles:
            save_cache(keyword, mode, articles)
            log_app_usage(f"[App] Cache Miss & Fetched: {keyword} ({mode})")  # <--- 記錄快取 miss
        else:
            st.warning("找不到相關文章")
            log_app_usage(f"[App] Fetch Failed: {keyword} ({mode})")
            articles = []

    if articles:
        texts = [clean_text(a["title"]) for a in articles]
        topics = extract_topics(texts, vectorizer)
        sentiments = [analyze_sentiments(t) for t in texts]
        suggestions = generate_business_suggestions(topics, sentiments)

        log_app_usage(f"[App] Analysis Completed: {keyword} ({mode})")  # <--- 記錄分析完成

        # --- Display Articles DataFrame ---
        st.subheader("📄 文章列表")
        articles_df = pd.DataFrame(articles)
        st.dataframe(articles_df, use_container_width=True)

        # --- Display Topics ---
        st.subheader("📝 主題建模結果")
        st.write(topics)

        # --- Sentiment Analysis ---
        st.subheader("📊 情緒分析結果")
        sentiment_df = pd.DataFrame({"標題": texts, "情緒分數": sentiments})
        st.dataframe(sentiment_df, use_container_width=True)

        # --- Sentiment Distribution Chart ---
        st.subheader("📈 情緒分佈長條圖")
        fig, ax = plt.subplots()
        sns.histplot(sentiments, bins=10, kde=True, ax=ax)
        ax.set_xlabel("情緒分數")
        ax.set_ylabel("文章數量")
        st.pyplot(fig)

        # --- Topic Co-occurrence Heatmap (Real Data) ---
        st.subheader("🗺️ 主題關聯熱力圖")
        word_pairs = []
        for topic in topics:
            words = topic.split()
            word_pairs.extend(itertools.combinations(words, 2))

        pair_counts = Counter(word_pairs)
        unique_words = sorted(set(itertools.chain.from_iterable(word_pairs)))

        co_occurrence_matrix = pd.DataFrame(0, index=unique_words, columns=unique_words)
        for (w1, w2), count in pair_counts.items():
            co_occurrence_matrix.at[w1, w2] = count
            co_occurrence_matrix.at[w2, w1] = count

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.heatmap(co_occurrence_matrix, annot=True, cmap="YlGnBu", ax=ax2)
        st.pyplot(fig2)

        # --- Business Suggestions ---
        st.subheader("💡 商業建議")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}. {suggestion}**")

        log_app_usage(f"[App] Suggestion Ready for: {keyword}")  # <--- 記錄建議完成

from modules.crawler import fetch_articles

result = fetch_articles("生成式AI", mode="ptt", limit=5)
print(result)
# --- Run the Streamlit app ---