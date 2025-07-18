# app.py
import streamlit as st
import json
from modules.nlp import clean_and_tokenize

# 模擬模組功能（避免未導入 micropip 等錯誤）
def mock_generate_topics(cleaned_texts):
    import plotly.graph_objects as go
    dummy_topics = ["AI應用", "市場行銷"]
    fig = go.Figure(go.Bar(x=dummy_topics, y=[10, 7]))
    return dummy_topics, fig

def mock_analyze_sentiment(texts):
    return {"正向": 60, "中立": 30, "負向": 10}

def mock_suggest(topics, sentiments):
    return [
        {"主題": t, "建議": "可以推出對應產品或服務", "模式": "訂閱制"} for t in topics
    ]

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
        topics, topic_vis = mock_generate_topics(cleaned_texts)

        # 5. 情緒分析
        sentiments = mock_analyze_sentiment(texts)

        # 6. 商業模式建議
        suggestions = mock_suggest(topics, sentiments)

    st.success("分析完成！")

    # 顯示結果
    st.subheader("📈 主題趨勢分析")
    st.plotly_chart(topic_vis)

    st.subheader("🎭 情緒分析結果")
    st.write(sentiments)

    st.subheader("💼 商業化建議")
    for s in suggestions:
        st.markdown(f"- **{s['主題']}**：{s['建議']} ({s['模式']})")
