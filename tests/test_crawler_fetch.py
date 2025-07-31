# test_crawler_fetch.py
import unittest
from unittest.mock import patch
from modules.crawler_fetch import fetch_articles

class TestCrawlerFetch(unittest.TestCase):

    def test_fetch_articles_ptt(self):
        keyword = "生成式AI"
        mode = "ptt"
        limit = 5

        result = fetch_articles(keyword, mode=mode, limit=limit)

        # 基本驗證：回傳是 list
        self.assertIsInstance(result, list)

        # 若有資料，驗證格式正確
        if result:
            print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (PTT Mode)")
            for article in result:
                print(f"- {article.get('title', 'No Title')}")
                self.assertIn("title", article)
                self.assertIn("link", article)
                self.assertIn("date", article)
        else:
            print("[WARNING] PTT 爬蟲沒有回傳資料（請檢查資料源或關鍵字）")

    @patch('modules.crawler.google_news_api_fetch')
    def test_fetch_articles_news_mock(self, mock_news_fetch):
        # Mock Google News 回傳假資料
        mock_news_fetch.return_value = [
            {"title": "Mock News 1", "link": "http://example.com/1", "date": "2025-07-30T12:00:00Z"},
            {"title": "Mock News 2", "link": "http://example.com/2", "date": "2025-07-30T13:00:00Z"}
        ]

        keyword = "生成式AI"
        mode = "news"
        limit = 5

        result = fetch_articles(keyword, mode=mode, limit=limit, api_key="DUMMY_KEY")

        self.assertIsInstance(result, list)

        if result:
            print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (News Mode - Mock)")
            for article in result:
                print(f"- {article.get('title', 'No Title')}")
                self.assertIn("title", article)
                self.assertIn("link", article)
                self.assertIn("date", article)
        else:
            print("[FAILED] Mock News 爬蟲沒有回傳任何資料")

if __name__ == '__main__':
    unittest.main()
