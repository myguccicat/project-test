# batch_crawler.py
import time
import json
import os
from datetime import datetime, timedelta
from modules.crawler import fetch_articles

# --- Cache Directory ---
CACHE_DIR = "cache"
USER_TRACK_FILE = f"{CACHE_DIR}/user_keywords.json"
os.makedirs(CACHE_DIR, exist_ok=True)

# --- Load User Keywords ---
def load_user_keywords():
    if os.path.exists(USER_TRACK_FILE):
        with open(USER_TRACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- Predefined Hot Keywords ---
HOT_KEYWORDS = ["生成式AI", "電動車", "綠能", "元宇宙", "區塊鏈"]

# --- Cache Cleanup Function ---
def clean_expired_cache(days=7):
    now = datetime.now()
    expired_count = 0
    for file in os.listdir(CACHE_DIR):
        if file.endswith(".json") and not file.startswith("user_keywords"):
            file_path = os.path.join(CACHE_DIR, file)
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - modified_time > timedelta(days=days):
                os.remove(file_path)
                expired_count += 1
                print(f"[Deleted] 過期快取 {file}")
    print(f"[Cleanup] 共刪除 {expired_count} 筆過期快取")

# --- Batch Fetch Function ---
def batch_fetch():
    print(f"[Batch Start] {datetime.now()}")
    # 清理過期快取
    clean_expired_cache(days=7)

    # 結合預設熱門與使用者自訂關鍵字
    keywords = list(set(HOT_KEYWORDS + load_user_keywords()))
    for keyword in keywords:
        for mode in ["ptt", "news"]:
            cache_file = f"{CACHE_DIR}/{keyword}_{mode}.json"
            # 若快取已存在且24小時內，則跳過
            if os.path.exists(cache_file):
                modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                if datetime.now() - modified_time < timedelta(hours=24):
                    print(f"[Skip] {keyword} ({mode}) 已在24小時內更新")
                    continue

            print(f"[Fetching] {keyword} ({mode})")
            api_key = os.getenv("NEWS_API_KEY") if mode == "news" else None
            articles = fetch_articles(keyword, mode=mode, limit=10, api_key=api_key)
            if articles:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(articles, f, ensure_ascii=False, indent=2)
                print(f"[Saved] {cache_file}")
            else:
                print(f"[Failed] 無法取得 {keyword} ({mode}) 資料")

    print(f"[Batch End] {datetime.now()}")

if __name__ == "__main__":
    while True:
        batch_fetch()
        time.sleep(86400)  # 每24小時執行一次
