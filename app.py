import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
from collections import Counter
import itertools
import io
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.io as pio
import xlsxwriter
import jieba
from sklearn.feature_extraction.text import CountVectorizer

# --- Custom Imports ---
from modules.crawler import fetch_articles
from modules.nlp import clean_text
from modules.topic_model import extract_topics
from modules.sentiment import analyze_sentiments, summarize_text
from modules.suggestion import generate_business_suggestions
from modules.utils import log_app_usage
from cache.cache_utils import load_cache, save_cache

# --- Global Settings ---
pio.templates.default = "plotly_white"
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False

# --- Load .env ---
load_dotenv()

# --- Streamlit App Config ---
st.set_page_config(page_title="趨勢分析與商業建議", layout="wide")
st.title("🔍 AI趨勢顧問")

# --- Get URL Parameters ---
query_params = st.query_params  # <-- 這裡不要加 ()
keyword = query_params.get("keyword", "")
mode = query_params.get("mode", ["ptt"])[0] if "mode" in query_params else "ptt" # 預設 ptt

# --- User Input Section ---
keyword = st.text_input("請輸入關鍵字:", value=keyword)
mode = st.selectbox("選擇資料來源:", ["ptt", "news"], index=0 if mode == "ptt" else 1)

# --- Display Current Keyword ---
if keyword:
    st.write(f"目前搜尋關鍵字：**{keyword}** (資料來源：**{mode}**)")
else:
    st.warning("請從 Django 或這裡輸入關鍵字再執行分析。")

# --- Run Analysis ---
if st.button("執行分析") and keyword:
    log_app_usage(f"[App] User Input Keyword: {keyword} ({mode})")
    cache_data = load_cache(keyword, mode)

    if cache_data:
        st.info("使用快取資料 (1 小時內最新)")
        articles = cache_data
        log_app_usage(f"[App] Cache Hit: {keyword} ({mode})")
    else:
        api_key = os.getenv("NEWS_API_KEY")
        articles = fetch_articles(keyword, mode=mode, limit=10, api_key=api_key)
        if articles:
            save_cache(keyword, mode, articles)
            log_app_usage(f"[App] Cache Miss & Fetched: {keyword} ({mode})")
        else:
            st.warning("找不到相關文章")
            log_app_usage(f"[App] Fetch Failed: {keyword} ({mode})")
            articles = []

    if articles:
        # --- NLP Processing ---
        texts = [clean_text(a["title"]) for a in articles]
        topics = extract_topics(texts, n_clusters=3)
        sentiment_result = analyze_sentiments(texts)
        sentiment_avg = sentiment_result["average"]
        suggestions = generate_business_suggestions(topics, sentiment_result["counts"], sentiment_avg)
        log_app_usage(f"[App] Analysis Completed: {keyword} ({mode})")

        # --- Display Articles ---
        st.subheader("📄 文章列表")
        articles_df = pd.DataFrame(articles)
        st.dataframe(articles_df, use_container_width=True)

        # --- Display Topics ---
        st.subheader("📝 主題建模結果")
        st.write(topics)

        # --- Sentiment Analysis Table ---
        st.subheader("📊 情緒分析結果")
        sentiment_df = pd.DataFrame([{
            "標題": d["title"],
            "情緒標籤": d["label"],
            "情緒分數": d["score"]
        } for d in sentiment_result["details"]])
        st.dataframe(sentiment_df, use_container_width=True)

        # --- Sentiment Distribution Chart ---
        st.subheader("📈 情緒分佈長條圖")
        fig, ax = plt.subplots()
        sns.histplot(sentiment_result["scores"], bins=10, kde=True, ax=ax)
        ax.set_xlabel("情緒分數")
        ax.set_ylabel("文章數量")
        st.pyplot(fig)

        # --- Drill-Down ---
        st.subheader("🔎 主題文章細節 Drill-down")
        selected_cluster = st.selectbox("選擇要檢視的 Cluster ID", [topic["cluster"] for topic in topics])

        for topic in topics:
            if topic["cluster"] == selected_cluster:
                st.markdown(f"### Cluster {topic['cluster']} — 關鍵字: {', '.join(topic['keywords'])}")
                for idx in topic["article_idxs"]:
                    detail = sentiment_result["details"][idx]
                    summary = summarize_text(detail["title"])
                    with st.expander(f"【{detail['label']}】{detail['title']} (分數: {detail['score']:.2f})"):
                        st.write(f"摘要：{summary}")

        # --- Export Cluster Report ---
        if st.button("📥 匯出該 Cluster 文章情緒報告"):
            export_data = []
            for topic in topics:
                if topic["cluster"] == selected_cluster:
                    for idx in topic["article_idxs"]:
                        detail = sentiment_result["details"][idx]
                        summary = summarize_text(detail["title"])
                        export_data.append({
                            "標題": detail["title"],
                            "情緒標籤": detail["label"],
                            "情緒分數": detail["score"],
                            "摘要": summary
                        })

            if export_data:
                export_df = pd.DataFrame(export_data)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    export_df.to_excel(writer, index=False, sheet_name='Cluster_Report')
                output.seek(0)
                st.download_button(
                    label="📄 下載 Excel 報告",
                    data=output,
                    file_name=f"Cluster_{selected_cluster}_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("該 Cluster 內沒有文章可以匯出。")

        # --- Co-occurrence Heatmap ---
        st.subheader("🗺️ 主題關聯熱力圖")
        word_pairs = list(itertools.chain.from_iterable(
            itertools.combinations(topic["keywords"], 2) for topic in topics
        ))
        pair_counts = Counter(word_pairs)
        unique_words = sorted(set(itertools.chain.from_iterable(word_pairs)))
        matrix = pd.DataFrame(0, index=unique_words, columns=unique_words)
        for (w1, w2), count in pair_counts.items():
            matrix.at[w1, w2] = count
            matrix.at[w2, w1] = count

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.heatmap(matrix, annot=True, cmap="YlGnBu", ax=ax2)
        st.pyplot(fig2)

        # --- Sentiment Summary Dashboard ---
        st.subheader("📊 主題情緒分佈 Dashboard 總結")
        summary_data = []
        for topic in topics:
            sentiments = [sentiment_result["details"][i]["label"] for i in topic["article_idxs"]]
            counts = Counter(sentiments)
            summary_data.append({
                "Cluster": topic["cluster"],
                "Keywords": ", ".join(topic["keywords"]),
                "正向": counts.get("正向", 0),
                "中立": counts.get("中立", 0),
                "負向": counts.get("負向", 0),
                "總數": len(topic["article_idxs"])
            })
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df)

        most_positive = summary_df.sort_values(by="正向", ascending=False).iloc[0]
        most_negative = summary_df.sort_values(by="負向", ascending=False).iloc[0]

        st.markdown(f"✅ **正向聲量最高主題：** Cluster {most_positive['Cluster']} ({most_positive['Keywords']}) — {most_positive['正向']} 篇")
        st.markdown(f"⚠️ **負向聲量最高主題：** Cluster {most_negative['Cluster']} ({most_negative['Keywords']}) — {most_negative['負向']} 篇")

        # --- Business Suggestions ---
        st.subheader("💡 商業建議")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}. {suggestion}**")
        log_app_usage(f"[App] Suggestion Ready for: {keyword}")

        # --- 2D Scatter Plot ---
        st.subheader("🖼️ Cluster 2D Scatter Plot (視覺化)")
        tokenized_texts = [' '.join(jieba.lcut(t)) for t in texts]
        X = CountVectorizer().fit_transform(tokenized_texts)
        X_pca = PCA(n_components=2).fit_transform(X.toarray())
        scatter_data = []
        for i, (x, y) in enumerate(X_pca):
            cluster_id = next((topic["cluster"] for topic in topics if i in topic["article_idxs"]), None)
            scatter_data.append({
                "標題": articles[i]["title"],
                "情緒標籤": sentiment_result["details"][i]["label"],
                "Cluster": cluster_id,
                "X": x,
                "Y": y
            })
        scatter_df = pd.DataFrame(scatter_data)
        fig3 = px.scatter(scatter_df, x="X", y="Y", color="Cluster",
                          hover_data=["標題", "情緒標籤"],
                          title="文章聚類分佈")
        st.plotly_chart(fig3, use_container_width=True)

        # --- Export Dashboard Summary ---
        if st.button("📥 匯出 Dashboard 總覽報告"):
            output_summary = io.BytesIO()
            with pd.ExcelWriter(output_summary, engine='xlsxwriter') as writer:
                summary_df.to_excel(writer, index=False, sheet_name='Dashboard_Summary')
            output_summary.seek(0)
            st.download_button(
                label="📊 下載 Dashboard 總覽報告",
                data=output_summary,
                file_name=f"Dashboard_Summary_{keyword}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
