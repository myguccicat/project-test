# test/test_suggestion.py
import unittest
from modules.suggestion import generate_suggestions

class TestSuggestionModule(unittest.TestCase):

    def test_generate_suggestions_basic(self):
        topics = ["生成式AI應用", "資安與監管", "內容創作平台"]
        sentiment_counts = {"正向": 12, "中立": 5, "負向": 3}
        sentiment_avg = 0.68

        suggestions = generate_suggestions(topics, sentiment_counts, sentiment_avg)

        self.assertEqual(len(suggestions), 3)
        for suggestion in suggestions:
            self.assertIn("主題", suggestion)
            self.assertIn("建議", suggestion)
            self.assertIn("模式", suggestion)
            self.assertIsInstance(suggestion["建議"], str)
            self.assertIsInstance(suggestion["模式"], str)

    def test_low_sentiment_score(self):
        topics = ["法規與風險"]
        sentiment_counts = {"正向": 1, "中立": 2, "負向": 7}
        sentiment_avg = 0.32

        suggestions = generate_suggestions(topics, sentiment_counts, sentiment_avg)
        self.assertEqual(suggestions[0]["模式"], "顧問服務 / B2B 解決方案")

    def test_high_sentiment_score(self):
        topics = ["創作者經濟"]
        sentiment_counts = {"正向": 10, "中立": 0, "負向": 0}
        sentiment_avg = 0.82

        suggestions = generate_suggestions(topics, sentiment_counts, sentiment_avg)
        self.assertEqual(suggestions[0]["模式"], "訂閱制 / 內容付費")

if __name__ == '__main__':
    unittest.main()
