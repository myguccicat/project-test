# app.py
import streamlit as st
import json
from modules.nlp import clean_and_tokenize
from modules.topic_model import generate_topics
from modules.sentiment import analyze_sentiments
from modules.suggestion import generate_suggestions

from plotly.graph_objects import Figure, Bar, Layout

st.set_page_config(page_title="AI 趨勢分析與商業建議", layout="wide")
st.title("🔍 關鍵字趨勢分析與商業建議 MVP")

# 1. 關鍵字輸入
keyword = st.text_input("請輸入欲分析的關鍵字：", "生成式AI")

if st.button("開始分析"):
    with st.spinner("正在抓取與處理資料中..."):
        # 2. 取得模擬文章資料
        with open("data/sample_articles.json", "r", encoding="utf-8") as f:
            articles = json.load(f)

        texts = [a["content"] for a in articles]

        # 3. NLP 預處理
        cleaned_texts = clean_and_tokenize(texts)

        # 4. 主題建模
        topics, topic_vis = generate_topics(cleaned_texts)

        # 5. 情緒分析（含比例與平均分數）
        sentiments_result = analyze_sentiments(texts)
        sentiment_counts = sentiments_result["counts"]
        sentiment_avg = sentiments_result["average"]

        # 6. 商業模式建議（正式模組）
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
