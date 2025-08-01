# batch_crawler.py
import time
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules.crawler import fetch_articles
from modules.utils import log_app_usage  # <-- 共用 log 函數

# --- Load API Key from .env ---
load_dotenv()

# --- Cache Directory ---
CACHE_DIR = "cache"
USER_TRACK_FILE = f"{CACHE_DIR}/user_keywords.json"
DASHBOARD_FILE = f"{CACHE_DIR}/cache_stats.json"
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
        if file.endswith(".json") and not file.startswith("user_keywords") and not file.startswith("cache_stats"):
            file_path = os.path.join(CACHE_DIR, file)
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - modified_time > timedelta(days=days):
                os.remove(file_path)
                expired_count += 1
                print(f"[Deleted] 過期快取 {file}")
    print(f"[Cleanup] 共刪除 {expired_count} 筆過期快取")
    return expired_count

# --- Update Dashboard Stats ---
def update_dashboard(stats):
    if os.path.exists(DASHBOARD_FILE):
        with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
            dashboard = json.load(f)
    else:
        dashboard = {"fetch_logs": [], "cache_hits": 0, "cache_misses": 0, "expired_deleted": 0}

    dashboard["fetch_logs"].append({
        "timestamp": datetime.now().isoformat(),
        "stats": stats
    })

    # 保留最近50筆紀錄
    dashboard["fetch_logs"] = dashboard["fetch_logs"][-50:]

    # 累加統計
    dashboard["cache_hits"] += stats["cache_hits"]
    dashboard["cache_misses"] += stats["cache_misses"]
    dashboard["expired_deleted"] += stats["expired_deleted"]

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, ensure_ascii=False, indent=2)

# --- Batch Fetch Function ---
def batch_fetch():
    print(f"[Batch Start] {datetime.now()}")
    stats = {"cache_hits": 0, "cache_misses": 0, "expired_deleted": 0}

    # 清理過期快取
    stats["expired_deleted"] = clean_expired_cache(days=7)

    # 結合熱門與使用者自訂關鍵字
    keywords = list(set(HOT_KEYWORDS + load_user_keywords()))
    for keyword in keywords:
        for mode in ["ptt", "news"]:
            cache_file = f"{CACHE_DIR}/{keyword}_{mode}.json"
            # 若快取已存在且24小時內，則計為命中
            if os.path.exists(cache_file):
                modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                if datetime.now() - modified_time < timedelta(hours=24):
                    print(f"[Cache Hit] {keyword} ({mode}) 已在24小時內更新")
                    stats["cache_hits"] += 1
                    log_app_usage(f"Cache Hit: {keyword} ({mode})")
                    continue

            print(f"[Fetching] {keyword} ({mode})")
            api_key = os.getenv("NEWS_API_KEY") if mode == "news" else None
            articles = fetch_articles(keyword, mode=mode, limit=10, api_key=api_key)
            if articles:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(articles, f, ensure_ascii=False, indent=2)
                print(f"[Saved] {cache_file}")
                stats["cache_misses"] += 1
                log_app_usage(f"Fetched & Cached: {keyword} ({mode}) - {len(articles)} articles")
            else:
                print(f"[Failed] 無法取得 {keyword} ({mode}) 資料")
                log_app_usage(f"Fetch Failed: {keyword} ({mode})")

    update_dashboard(stats)
    print(f"[Batch End] {datetime.now()}")
    print(f"[Stats] Cache Hits: {stats['cache_hits']}, Misses: {stats['cache_misses']}, Deleted: {stats['expired_deleted']}")

if __name__ == "__main__":
    while True:
        batch_fetch()
        time.sleep(86400)  # 每24小時執行一次
