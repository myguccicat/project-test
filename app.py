# app.py
import streamlit as st
import json
import os
from datetime import datetime, timedelta

from modules.nlp import clean_and_tokenize
from modules.topic_model import generate_topics
from modules.sentiment import analyze_sentiments
from modules.suggestion import generate_suggestions
from modules.crawler import fetch_articles

from plotly.graph_objects import Figure, Bar, Layout

st.set_page_config(page_title="AI 趨勢分析與商業建議", layout="wide")
st.title("🔍 關鍵字趨勢分析與商業建議 MVP")

# --- Cache Utilities ---
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def load_cache(keyword, mode):
    cache_file = f"{CACHE_DIR}/{keyword}_{mode}.json"
    if os.path.exists(cache_file):
        modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - modified_time < timedelta(hours=1):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
    return None

def save_cache(keyword, mode, data):
    cache_file = f"{CACHE_DIR}/{keyword}_{mode}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- UI ---
keyword = st.text_input("請輸入欲分析的關鍵字：", "生成式AI")
mode = st.selectbox("選擇資料來源：", ["mock", "ptt", "news"], index=0)
api_key = None
if mode == "news":
    api_key = st.text_input("請輸入 Google News API Key：", type="password")

if st.button("開始分析"):
    with st.spinner("正在抓取與處理資料中..."):
        cache_data = load_cache(keyword, mode)
        if cache_data:
            st.info("使用快取資料 (1 小時內最新)")
            articles = cache_data
        else:
            articles = fetch_articles(keyword, mode=mode, limit=10, api_key=api_key)
            if articles:
                save_cache(keyword, mode, articles)

        if not articles:
            st.error("未能取得相關文章，請更換關鍵字或來源/API Key。")
        else:
            texts = [a["content"] for a in articles]

            # NLP 預處理
            cleaned_texts = clean_and_tokenize(texts)

            # 主題建模
            topics, topic_vis = generate_topics(cleaned_texts)

            # 情緒分析
            sentiments_result = analyze_sentiments(texts)
            sentiment_counts = sentiments_result["counts"]
            sentiment_avg = sentiments_result["average"]

            # 商業建議
            suggestions = generate_suggestions(topics, sentiment_counts, sentiment_avg)

    st.success("分析完成！")

    # 顯示結果
    st.subheader("📈 主題趨勢分析")
    st.plotly_chart(topic_vis)

    st.subheader("🎭 情緒分析結果")
    st.markdown(f"**平均情緒分數**：{sentiment_avg:.2f}")

    fig = Figure(
        data=[
            Bar(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), marker_color=['red','gray','green'])
        ],
        layout=Layout(
            title="情緒分佈圖",
            xaxis=dict(title="情緒類型"),
            yaxis=dict(title="文章數量")
        )
    )
    st.plotly_chart(fig)

    st.subheader("💼 商業化建議")
    for s in suggestions:
        st.markdown(f"- **{s['主題']}**：{s['建議']} ({s['模式']})")
