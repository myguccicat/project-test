@echo off
REM 啟動 Python 虛擬環境 (如有需要可開啟)
REM call venv\Scripts\activate

echo [1/4] 更新快取資料 (執行 batch_crawler.py)
python batch_crawler.py

echo [2/4] 啟動主應用 (app.py)
start cmd /k "streamlit run app.py"

echo [3/4] 啟動快取效能 Dashboard (cache_dashboard.py)
start cmd /k "streamlit run cache_dashboard.py"

echo [4/4] 執行單元測試 (tests/)
pytest tests/

echo ========================
echo ✅ 專案已啟動完成
echo - app.py 頁面預設: http://localhost:8501
echo - Dashboard 頁面預設: http://localhost:8502
echo ========================

pause
