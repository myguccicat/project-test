@echo off
echo 啟動 Django Server...
start cmd /k "conda activate django310 && python manage.py runserver"

timeout /t 3

echo 啟動 Streamlit App...
start cmd /k "conda activate django310 && streamlit run app.py --server.headless true"

echo 啟動完成，請瀏覽 http://localhost:8000/
pause
