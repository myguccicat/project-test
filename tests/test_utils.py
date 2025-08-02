import os
from modules.utils import log_app_usage, cache_stats

def test_log_app_usage(tmp_path):
    log_file = tmp_path / "test_log.log"
    original_log_path = "cache/app_usage.log"

    # 暫時更換 log 檔路徑
    os.makedirs("cache", exist_ok=True)
    os.rename(original_log_path, original_log_path + ".bak") if os.path.exists(original_log_path) else None
    try:
        # 測試 log 寫入
        log_app_usage("Test log entry")
        assert os.path.exists(original_log_path)
        with open(original_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert any("Test log entry" in line for line in lines)
    finally:
        # 還原
        if os.path.exists(original_log_path + ".bak"):
            os.remove(original_log_path)
            os.rename(original_log_path + ".bak", original_log_path)

def test_cache_stats():
    stats = cache_stats()
    assert "cache_hits" in stats
    assert "cache_misses" in stats
    assert "last_updated" in stats
