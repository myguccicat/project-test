# modules/crawler.py
import time
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# --- Load API Key from .env ---
load_dotenv()

# --- PTT Mock Data Function ---
def crawl_ptt_data(keyword, limit):
    articles = []
    base_url = 'https://www.ptt.cc/bbs/Gossiping/index.html' # PTT Gossiping 第一頁網址
    current_page_url = base_url
    
    rs = requests.session()
    # 處理 18 禁頁面
    res = rs.get(base_url, verify=True, timeout=10)
    if "over18" in res.url:
        print("偵測到 18 禁頁面，嘗試進入並設定 timeout...")
        data = {
            'from': '/bbs/Gossiping/index.html',
            'yes': 'yes'
        }
        try:
            rs.post('https://www.ptt.cc/ask/over18', data=data, verify=True, timeout=10)
            res = rs.get(base_url, verify=True, timeout=10) # 重新取得頁面
        except requests.exceptions.RequestException as e:
            print(f"處理 18 禁頁面時發生請求錯誤: {e}")
            return []

    while len(articles) < limit:
        print(f"正在爬取頁面: {current_page_url}, 已抓取文章數: {len(articles)}")
        try:
            response = rs.get(current_page_url, timeout=10)
            response.raise_for_status() # 檢查 HTTP 錯誤
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取文章列表
            articles_on_page = 0
            for article_div in soup.find_all('div', class_='r-ent'):
                title_element = article_div.find('div', class_='title')
                if title_element and title_element.find('a'):
                    title = title_element.find('a').text.strip()
                    article_url = 'https://www.ptt.cc' + title_element.find('a')['href']
                    article_data = crawl_single_article(article_url)
                    # 根據關鍵字過濾
                    if keyword.lower() in title.lower() or keyword.lower() in article_data.get("content", "").lower():
                        articles.append({
                            "title": title,
                            "link": article_url,
                            "date": article_data.get("date", ""),
                            "author": article_data.get("author", ""),
                            "push": article_data.get("push", ""),
                            "content": article_data.get("content", "")
                        })
                        articles_on_page += 1
                        print(f"  - 找到文章: '{title}', 當前總數: {len(articles)}")
                        if len(articles) >= limit:
                            break # 達到限制後立即停止

            # 檢查是否已達到限制，如果達到則停止
            if len(articles) >= limit:
                break

            # 找到上一頁的連結
            prev_page_button = None
            paging_div = soup.find('div', class_='btn-group btn-group-ptt-paging')
            if paging_div:
                # 優先從 btn-group-ptt-paging 中尋找「‹ 上頁」按鈕
                for button in paging_div.find_all('a', class_='btn wide'):
                    if '‹ 上頁' in button.text:
                        prev_page_button = button
                        break
            
            # 如果沒有在特定分頁組中找到，則嘗試更通用的方法
            if not prev_page_button:
                for a_tag in soup.find_all('a'):
                    if '‹ 上頁' in a_tag.text or '上頁' in a_tag.text:
                        prev_page_button = a_tag
                        break

            if prev_page_button and 'href' in prev_page_button.attrs:
                current_page_url = 'https://www.ptt.cc' + prev_page_button['href']
            else:
                print("沒有找到 '‹ 上頁' 或 '上頁' 連結，結束爬取。")
                break # 沒有上一頁了
        except requests.exceptions.HTTPError as e:
            print(f"PTT HTTP 錯誤: {e.response.status_code} - {e.response.text}")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"PTT 連線錯誤: {e}")
            break
        except requests.exceptions.Timeout as e:
            print(f"PTT 請求超時: {e}")
            break
        except requests.exceptions.RequestException as e:
            print(f"PTT 請求發生未知錯誤: {e}")
            break
        except Exception as e:
            print(f"PTT 爬取過程中發生意外錯誤: {e}")
            break
        time.sleep(0.3) # 避免頻繁請求被鎖
    return articles

def crawl_single_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # 檢查 HTTP 錯誤
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到文章內容
        content_element = soup.find('div', id='main-content')
        if content_element:
            # 提取文章資訊 (作者、標題、時間)
            author = ""
            title = ""
            date = ""
            for meta in content_element.find_all('div', class_='article-meta-value'):
                if meta.previous_sibling and meta.previous_sibling.text and "作者" in meta.previous_sibling.text:
                    author = meta.text.strip()
                elif meta.previous_sibling and meta.previous_sibling.text and "標題" in meta.previous_sibling.text:
                    title = meta.text.strip()
                elif meta.previous_sibling and meta.previous_sibling.text and "時間" in meta.previous_sibling.text:
                    date = meta.text.strip()

            # 提取推文數 (需要遍歷推文區塊)
            push_count = 0
            for push_tag in content_element.find_all('div', class_='push'):
                if push_tag.find('span', class_='push-tag') and '推' in push_tag.find('span', class_='push-tag').text:
                    push_count += 1
                elif push_tag.find('span', class_='push-tag') and '噓' in push_tag.find('span', class_='push-tag').text:
                    push_count -= 1 # 噓文算負分

            # 去除不必要的內容
            for div in content_element.find_all('div', class_='article-metaline'):
                div.decompose()
            for div in content_element.find_all('div', class_='article-metaline-right'):
                div.decompose()
            for div in content_element.find_all('div', class_='push'):
                div.decompose()
            
            # 提取文字
            content = content_element.text.strip()
            # 移除多餘的符號
            content = content.split('--')[0] # 移除--之後的內容
            return {"content": content, "author": author, "date": date, "push": push_count}
        else:
            print(f"無法在 {url} 找到文章內容。")
            return {"content": "找不到內容", "author": "", "date": "", "push": ""}
    except requests.exceptions.HTTPError as e:
        print(f"取得單篇文章 {url} 時發生 HTTP 錯誤: {e.response.status_code} - {e.response.text}")
        return {"content": f"HTTP 錯誤: {e.response.status_code}", "author": "", "date": "", "push": ""}
    except requests.exceptions.ConnectionError as e:
        print(f"取得單篇文章 {url} 時發生連線錯誤: {e}")
        return {"content": f"連線錯誤: {e}", "author": "", "date": "", "push": ""}
    except requests.exceptions.Timeout as e:
        print(f"取得單篇文章 {url} 時請求超時: {e}")
        return {"content": f"請求超時: {e}", "author": "", "date": "", "push": ""}
    except requests.exceptions.RequestException as e:
        print(f"取得單篇文章 {url} 時發生未知請求錯誤: {e}")
        return {"content": f"未知請求錯誤: {e}", "author": "", "date": "", "push": ""}
    except Exception as e:
        print(f"取得單篇文章 {url} 時發生意外錯誤: {e}")
        return {"content": f"意外錯誤: {e}", "author": "", "date": "", "push": ""}

# --- Google News API Fetch Function ---
def google_news_api_fetch(keyword, limit, api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "language": "zh",
        "pageSize": limit,
        "apiKey": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", "No Title"),
                "link": article.get("url", ""),
                "date": article.get("publishedAt", ""),
                "content": article.get("description", "No Content")  # 你測試裡有驗證 content
            })
        return articles
    except Exception as e:
        print(f"[Error] Google News API 請求失敗: {e}")
        return []

# --- Main Fetch Function ---
def fetch_articles(keyword, mode="ptt", limit=10, api_key=None):
    if mode == "ptt":
        articles = crawl_ptt_data(keyword, limit)
    elif mode == "news":
        api_key = api_key or os.getenv("NEWS_API_KEY")
        if api_key:
            articles = google_news_api_fetch(keyword, limit, api_key)
        else:
            print("[Error] 缺少 Google News API 金鑰")
            articles = []
    else:
        articles = []

    return articles

