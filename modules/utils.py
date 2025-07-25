# --- App Usage Logger ---
def log_app_usage(message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"
    with open(APP_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())
