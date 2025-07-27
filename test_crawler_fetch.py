# test_crawler_fetch.py

from modules.crawler import fetch_articles

# 測試關鍵字
keyword = "生成式AI"
mode = "ptt"  # 可改為 "news" 測試 Google News API
limit = 5

# 呼叫爬蟲 function
result = fetch_articles(keyword, mode=mode, limit=limit)

# 輸出結果
if result:
    print(f"[SUCCESS] 爬取到 {len(result)} 筆資料")
    for article in result:
        print(f"- {article.get('title', 'No Title')}")
else:
    print("[FAILED] 爬蟲沒有回傳任何資料")
