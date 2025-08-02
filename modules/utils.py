import os
from datetime import datetime

APP_LOG_FILE = "cache/app_usage.log"

def log_app_usage(message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"
    os.makedirs(os.path.dirname(APP_LOG_FILE), exist_ok=True)
    with open(APP_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())

def cache_stats():
    """
    模擬回傳 Cache 統計資訊。
    """
    return {
        "cache_hits": 12,
        "cache_misses": 3,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
