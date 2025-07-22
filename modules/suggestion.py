# modules/suggestion.py
def generate_suggestions(topics, sentiment_counts, sentiment_avg):
    """
    根據主題、情緒分佈與平均情緒分數，產出商業建議。
    回傳格式：[{主題, 建議, 模式}]
    """

    def pick_model(score):
        if score > 0.7:
            return "訂閱制 / 內容付費"
        elif score > 0.4:
            return "廣告收入 / 聯盟行銷"
        else:
            return "顧問服務 / B2B 解決方案"

    suggestions = []

    for topic in topics:
        score = sentiment_avg
        mode = pick_model(score)

        # 簡單關鍵字比對推薦（可未來替換為 GPT 模型）
        if "監管" in topic or "法規" in topic:
            idea = "可針對法規風險提供付費合規顧問"
        elif "創作" in topic or "生成" in topic:
            idea = "可推出創作工具或內容平台收費服務"
        elif "產業" in topic or "應用" in topic:
            idea = "可進行垂直領域解決方案銷售"
        elif "資安" in topic or "資料" in topic:
            idea = "提供企業資安諮詢或資料管理方案"
        else:
            idea = "可考慮透過數據平台提供商業洞察服務"

        suggestions.append({
            "主題": topic,
            "建議": idea,
            "模式": mode
        })

    return suggestions
