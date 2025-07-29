def generate_business_suggestions(topics, sentiment_counts, sentiment_avg):
    suggestions = []

    # --- 總體情緒判斷 ---
    if sentiment_avg > 0.66:
        suggestions.append("整體情緒偏正向，可以考慮推出促銷活動強化品牌聲量。")
    elif sentiment_avg < 0.33:
        suggestions.append("整體情緒偏負向，需注意品牌形象與負評聲量。")
    else:
        suggestions.append("整體情緒偏中立，可以透過專業內容行銷提高正面關注度。")

    # --- 負向情緒處理建議 ---
    if sentiment_counts.get("負向", 0) > sentiment_counts.get("正向", 0):
        suggestions.append("負向情緒比重大，建議針對用戶反饋進行深度調查與公關危機處理。")

    # --- 針對每個主題額外分析 (情緒分佈 dashboard 會用的) ---
    for topic in topics:
        cluster_id = topic["cluster"]
        keywords = ", ".join(topic["keywords"])
        # 這裡可擴充條件式來依據主題關鍵字給個別建議
        if any(word in keywords for word in ["投訴", "問題", "負評"]):
            suggestions.append(f"Cluster {cluster_id} ({keywords}) 相關主題需加強售後服務與負評回應策略。")

    return suggestions
