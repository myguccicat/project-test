import unittest
from unittest.mock import patch, Mock
from modules.crawler import fetch_articles

class TestCrawlerFetch(unittest.TestCase):

    def test_fetch_articles_ptt(self):
        keyword = "生成式AI"
        mode = "ptt"
        limit = 5

        result = fetch_articles(keyword, mode=mode, limit=limit)

        self.assertIsInstance(result, list)
        if result:
            print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (PTT Mode)")
            for article in result:
                print(f"- {article.get('title', 'No Title')}")
                self.assertIn("title", article)
                self.assertIn("link", article)
                self.assertIn("date", article)
                self.assertIn("content", article)
        else:
            print("[WARNING] PTT 爬蟲沒有回傳資料")

    @patch('modules.crawler.requests.get')
    def test_fetch_articles_news_api_error(self, mock_get):
         # 模擬 API 回傳 500 錯誤
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = fetch_articles("生成式AI", mode="news", limit=5, api_key="DUMMY_KEY")
        self.assertEqual(result, [])  # 應回傳空list

        print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (News Mode - Mock)")
        for article in result:
            print(f"- {article.get('title', 'No Title')}")
            self.assertIn("title", article)
            self.assertIn("link", article)
            self.assertIn("date", article)
           
    def test_fetch_articles_invalid_mode(self):
        result = fetch_articles("生成式AI", mode="invalid_mode", limit=5)
        self.assertEqual(result, [])  # 無效mode應該回傳空list

if __name__ == '__main__':
    unittest.main()
