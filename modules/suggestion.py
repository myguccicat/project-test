def generate_business_suggestions(topics, sentiment_counts, sentiment_avg):
    suggestions = []

    # --- 總體情緒判斷 ---
    if sentiment_avg > 0.66:
        suggestions.append({"主題": "整體情緒",
                            "建議": "整體情緒偏正向，可以考慮推出促銷活動強化品牌聲量。",
                            "模式": "訂閱制 / 內容付費"})
    elif sentiment_avg < 0.33:
        suggestions.append({"主題": "整體情緒",
                            "建議": "整體情緒偏負向，需注意品牌形象與負評聲量。",
                            "模式": "顧問服務 / B2B 解決方案"})
    else:
        suggestions.append({"主題": "整體情緒",
                            "建議": "整體情緒偏中立，可以透過活動增加互動與討論度。",
                            "模式": "活動行銷 / 社群互動"})

    # --- 負向情緒處理建議 ---
    if sentiment_counts.get("負向", 0) > sentiment_counts.get("正向", 0):
        suggestions.append({"主題": "品牌負評",
                            "建議": "負向情緒比重大，建議針對用戶反饋進行深度調查與公關危機處理。",
                            "模式": "品牌修復計畫"})

    # --- 針對每個主題額外分析 ---
    for topic in topics:
        cluster_id = topic.get("cluster", 0)
        keywords = ", ".join(topic["keywords"])
        if any(word in keywords for word in ["投訴", "問題", "負評"]):
            suggestions.append({
                "主題": f"Cluster {cluster_id} ({topic['topic']})",
                "建議": f"Cluster {cluster_id} ({keywords}) 相關主題需加強售後服務與負評回應策略。",
                "模式": "客戶服務優化"
            })

    return suggestions
