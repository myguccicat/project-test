@echo off
REM === 啟動 conda 環境 ===
CALL conda activate django

REM === 切換到專案資料夾 ===
cd /d %~dp0

REM === 安裝 requirements.txt 所需套件 ===
pip install -r requirements.txt

echo [1/4] 更新快取資料 (執行 batch_crawler.py)
start cmd /k "python batch_crawler.py"

echo [2/4] 啟動主應用 (app.py)
start cmd /k "streamlit run app.py"

echo [3/4] 啟動快取效能 Dashboard (cache_dashboard.py)
start cmd /k "streamlit run pages/cache_dashboard.py"

echo [4/4] 執行單元測試 (tests/)
start cmd /k "pytest tests/"

echo ========================
echo ✅ 專案已啟動完成
echo - app.py 頁面預設: http://localhost:8501
echo - Dashboard 頁面預設: http://localhost:8502
echo ========================

pause
