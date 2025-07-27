# --- App Usage Logger ---
from datetime import datetime
APP_LOG_FILE = "cache/app_usage.log"
# --- 記錄應用程式使用情況 ---
# 每次使用者操作都會記錄到這個檔案中，方便後續分析使用情況

def log_app_usage(message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"
    with open(APP_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())
