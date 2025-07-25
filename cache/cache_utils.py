# cache/cache_utils.py
import os
import json
from datetime import datetime, timedelta

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# --- 載入快取資料 (1小時有效期) ---
def load_cache(keyword, mode):
    cache_file = os.path.join(CACHE_DIR, f"{keyword}_{mode}.json")
    if os.path.exists(cache_file):
        modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - modified_time < timedelta(hours=1):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
    return None

# --- 儲存快取資料 ---
def save_cache(keyword, mode, data):
    cache_file = os.path.join(CACHE_DIR, f"{keyword}_{mode}.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- 快取是否過期 (for batch_crawler use) ---
def is_cache_valid(cache_file, hours=24):
    if os.path.exists(cache_file):
        modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - modified_time < timedelta(hours=hours):
            return True
    return False

# --- 讀取使用者追蹤的關鍵字清單 ---
def load_user_keywords(user_track_file="cache/user_keywords.json"):
    if os.path.exists(user_track_file):
        with open(user_track_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
