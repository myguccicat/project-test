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
        "link": f"https://www.ptt.cc/bbs/Board/{i}.html",
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
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"[Error] Google News API 回應錯誤: {response.status_code}")
        return []

    data = response.json()
    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title", "No Title"),
            "link": article.get("url", ""),
            "date": article.get("publishedAt", "")
        })
    return articles
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

except requests.RequestException as e:
    print(f"[Error] Google News API 請求失敗: {e}")

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

# --- For Testing ---
if __name__ == "__main__":
    print("[Demo] PTT Mock Data")
    print(fetch_articles("生成式AI", mode="ptt", limit=3))
    print("[Demo] Google News API")
    print(fetch_articles("區塊鏈", mode="news", limit=3))
