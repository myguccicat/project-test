# modules/crawler.py
import time
import requests
import os
from dotenv import load_dotenv

# --- Load API Key from .env ---
load_dotenv()

# --- PTT Mock Data Function ---
def mock_ptt_data(keyword, limit):
    return [{
        "title": f"[PTT] {keyword} 熱門文章 {i}",
        "link": f"https://www.ptt.cc/bbs/Gossiping/{i}.html",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),  # 模擬日期
        "content": f"這是關於 {keyword} 的文章內容 {i}。"
    } for i in range(1, limit + 1)]

# --- Google News API Fetch Function ---
def google_news_api_fetch(keyword, limit, api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "language": "zh",
        "pageSize": limit,
        "apiKey": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", "No Title"),
                "link": article.get("url", ""),
                "date": article.get("publishedAt", ""),
                "content": article.get("description", "No Content")  # 你測試裡有驗證 content
            })
        return articles
    except Exception as e:
        print(f"[Error] Google News API 請求失敗: {e}")
        return []

# --- Main Fetch Function ---
def fetch_articles(keyword, mode="ptt", limit=10, api_key=None):
    if mode == "ptt":
        articles = mock_ptt_data(keyword, limit)
    elif mode == "news":
        api_key = api_key or os.getenv("NEWS_API_KEY")
        if api_key:
            articles = google_news_api_fetch(keyword, limit, api_key)
        else:
            print("[Error] 缺少 Google News API 金鑰")
            articles = []
    else:
        articles = []

    return articles

