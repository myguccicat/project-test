# modules/crawler.py
import requests
from bs4 import BeautifulSoup
import random

def fetch_ptt_articles(keyword, limit=10):
    """
    簡易 PTT 爬蟲：搜尋指定關鍵字並抓取文章內容
    """
    base_url = "https://www.ptt.cc"
    search_url = f"{base_url}/bbs/Gossiping/search?q={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('div.title a')

    articles = []
    for link in links[:limit]:
        href = link['href']
        article_url = base_url + href
        article_res = requests.get(article_url, headers=headers)
        if article_res.status_code != 200:
            continue

        article_soup = BeautifulSoup(article_res.text, 'html.parser')
        content = article_soup.select_one('#main-content').text
        content = content.split('--')[0]  # 移除留言區
        articles.append({"content": content.strip()})

    return articles

def fetch_mock_articles(keyword, limit=10):
    """
    模擬爬取 PTT / 新聞資料 (之後可換成真實爬蟲)
    """
    mock_data = [
        f"{keyword} 引起了熱烈討論，許多專家認為將徹底改變產業。",
        f"近期有關 {keyword} 的監管問題備受關注，市場反應不一。",
        f"{keyword} 應用於創作與設計領域，吸引了大量創業公司投入。",
        f"分析指出 {keyword} 將帶動新一波商業模式變革。",
        f"部分用戶對 {keyword} 的隱私疑慮仍未獲得有效解決。",
        f"{keyword} 在教育與培訓市場潛力巨大，業者積極佈局。",
        f"企業對於 {keyword} 的導入態度趨於保守，需要更多案例驗證。",
        f"{keyword} 資安風險浮上檯面，專家呼籲強化防護措施。",
        f"{keyword} 技術創新速度驚人，法規制定進度亟待跟上。",
        f"{keyword} 相關投資正在快速增加，市場熱度持續升高。"
    ]

    random.shuffle(mock_data)
    return [{"content": text} for text in mock_data[:limit]]

def fetch_articles(keyword, mode="mock", limit=10):
    """
    根據 mode ('mock' or 'ptt') 切換爬取來源
    """
    if mode == "ptt":
        return fetch_ptt_articles(keyword, limit)
    else:
        return fetch_mock_articles(keyword, limit)
