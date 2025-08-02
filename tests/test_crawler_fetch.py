# tests/test_crawler_fetch.py
# import pytest
# import unittest
# from unittest.mock import patch, MagicMock
# from modules.crawler import fetch_articles, google_news_api_fetch, mock_ptt_data

# class TestCrawlerFetch(unittest.TestCase):

#     def test_fetch_articles_ptt(self):
#         keyword = "生成式AI"
#         mode = "ptt"
#         limit = 5

#         result = fetch_articles(keyword, mode=mode, limit=limit)

#         self.assertIsInstance(result, list)
#         if result:
#             print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (PTT Mode)")
#             for article in result:
#                 print(f"- {article.get('title', 'No Title')}")
#                 self.assertIn("title", article)
#                 self.assertIn("link", article)
#                 self.assertIn("date", article)
#                 self.assertIn("content", article)
#         else:
#             print("[WARNING] PTT 爬蟲沒有回傳資料")

# class TestCrawlerFetchExtended(unittest.TestCase):

#     @patch('modules.crawler.requests.get')
#     def test_fetch_articles_news_api_error(self, mock_get):
#          # 模擬 API 回傳 500 錯誤
#         mock_response = MagicMock()
#         mock_response.status_code = 500
#         mock_response.json.return_value = {}
#         mock_get.return_value = mock_response

#         result = fetch_articles("生成式AI", mode="news", limit=5, api_key="DUMMY_KEY")
#         self.assertEqual(result, [])  # 應回傳空list

#         print(f"[SUCCESS] 爬取到 {len(result)} 筆資料 (News Mode - Mock)")
#         for article in result:
#             print(f"- {article.get('title', 'No Title')}")
#             self.assertIn("title", article)
#             self.assertIn("link", article)
#             self.assertIn("date", article)
#             self.assertIn("content", article)
           
#     def test_fetch_articles_invalid_mode(self):
#         result = fetch_articles("生成式AI", mode="invalid_mode", limit=5)
#         self.assertEqual(result, [])  # 無效mode應該回傳空list

#     @patch('modules.crawler.requests.get', side_effect=Exception("Connection error"))
#     def test_fetch_articles_news_request_exception(self, mock_get):
#         result = fetch_articles("生成式AI", mode="news", limit=5, api_key="DUMMY_KEY")
#         self.assertEqual(result, [])

#     @patch('modules.crawler.requests.get')
#     def test_fetch_articles_news_success(self, mock_get):
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             "status": "ok",
#             "articles": [
#                 {
#                     "title": "生成式AI新聞",
#                     "description": "這是一則新聞描述",
#                     "url": "http://example.com",
#                     "publishedAt": "2025-08-02T12:00:00Z"
#                 }
#             ]
#         }
#         mock_get.return_value = mock_response

#         result = fetch_articles("生成式AI", mode="news", limit=1, api_key="DUMMY_KEY")
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["title"], "生成式AI新聞")
#         self.assertEqual(result[0]["link"], "http://example.com")

# if __name__ == '__main__':
#     unittest.main()
import unittest
from unittest.mock import patch, MagicMock
from modules.crawler import fetch_articles, google_news_api_fetch, mock_ptt_data

class TestCrawlerFetch(unittest.TestCase):

    def test_fetch_articles_ptt(self):
        keyword = "生成式AI"
        result = fetch_articles(keyword, mode="ptt", limit=3)
        self.assertEqual(len(result), 3)
        self.assertIn("title", result[0])
        self.assertIn("link", result[0])
        self.assertIn("date", result[0])
        self.assertIn("content", result[0])

    @patch('modules.crawler.requests.get')
    def test_google_news_api_fetch_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "articles": [
                {
                    "title": "Test News",
                    "url": "http://example.com",
                    "publishedAt": "2025-08-02T12:00:00Z",
                    "description": "News Content"
                }
            ]
        }
        mock_get.return_value = mock_response

        result = google_news_api_fetch("AI", 1, api_key="DUMMY_KEY")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test News")

    @patch('modules.crawler.requests.get')
    def test_google_news_api_fetch_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection Error")
        result = google_news_api_fetch("AI", 1, api_key="DUMMY_KEY")
        self.assertEqual(result, [])

    def test_fetch_articles_invalid_mode(self):
        result = fetch_articles("AI", mode="invalid", limit=3)
        self.assertEqual(result, [])

    @patch('modules.crawler.google_news_api_fetch', return_value=[{"title": "News", "link": "link", "date": "date", "content": "content"}])
    def test_fetch_articles_news_with_key(self, mock_fetch):
        result = fetch_articles("AI", mode="news", limit=1, api_key="DUMMY_KEY")
        self.assertEqual(len(result), 1)

    @patch('modules.crawler.os.getenv', return_value=None)
    def test_fetch_articles_news_no_api_key(self, mock_getenv):
        result = fetch_articles("AI", mode="news", limit=1)
        self.assertEqual(result, [])
    
if __name__ == "__main__":
    unittest.main()
