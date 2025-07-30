# pages/cache_dashboard.py
"""
Cache Dashboard for monitoring cache statistics and app usage logs.
This page provides insights into cache hits, misses, and historical fetch logs.
"""
import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- Load Cache Stats ---
CACHE_STATS_FILE = "cache/cache_stats.json"
APP_LOG_FILE = "cache/app_usage.log"

st.set_page_config(page_title="快取與使用紀錄 Dashboard", layout="wide")
st.title("📊 快取狀況與使用紀錄 Dashboard")

# --- Load Cache Stats Data ---
if os.path.exists(CACHE_STATS_FILE):
    with open(CACHE_STATS_FILE, "r", encoding="utf-8") as f:
        stats_data = json.load(f)
else:
    stats_data = {"fetch_logs": [], "cache_hits": 0, "cache_misses": 0, "expired_deleted": 0}

# --- Display Summary Stats ---
st.subheader("📋 總體統計數據")
st.metric("快取命中次數", stats_data.get("cache_hits", 0))
st.metric("快取失敗次數", stats_data.get("cache_misses", 0))
st.metric("過期快取刪除數", stats_data.get("expired_deleted", 0))

# --- Fetch Logs Table ---
fetch_logs = stats_data.get("fetch_logs", [])
if fetch_logs:
    logs_df = pd.DataFrame([
        {"時間": log["timestamp"],
         "命中": log["stats"]["cache_hits"],
         "失敗": log["stats"]["cache_misses"],
         "刪除": log["stats"]["expired_deleted"]} for log in fetch_logs
    ])

    st.subheader("🕒 批次爬蟲歷史紀錄")
    st.dataframe(logs_df, use_container_width=True)

    # --- Line Chart: Cache Hit/Miss Over Time ---
    st.subheader("📈 命中 / 失敗 數量趨勢圖")
    logs_df["時間"] = pd.to_datetime(logs_df["時間"])
    logs_df = logs_df.sort_values("時間")

    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(logs_df["時間"], logs_df["命中"], label="Cache Hit", marker="o")
    ax1.plot(logs_df["時間"], logs_df["失敗"], label="Cache Miss", marker="x")
    ax1.set_xlabel("時間")
    ax1.set_ylabel("次數")
    ax1.legend()
    st.pyplot(fig1)

# --- App Usage Log Viewer ---
st.subheader("📄 分析執行歷史紀錄 (最近100筆)")
if os.path.exists(APP_LOG_FILE):
    with open(APP_LOG_FILE, "r", encoding="utf-8") as f:
        log_lines = f.readlines()[-100:]
    for line in reversed(log_lines):
        st.text(line.strip())
else:
    st.write("無使用紀錄")
