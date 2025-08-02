# tests/test_suggestion.py
import pytest
import unittest
from modules.suggestion import generate_business_suggestions

class TestSuggestionModule(unittest.TestCase):

    def test_generate_suggestions_basic(self):
        topics = [{"topic": "生成式AI應用", "cluster": 1, "keywords": ["AI", "問題", "應用"]}, 
                  {"topic": "資安與監管", "cluster": 2, "keywords": ["資安", "監管", "負評"]}]
        sentiment_counts = {"正向": 12, "中立": 5, "負向": 3}
        sentiment_avg = 0.68

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)
        
        self.assertEqual(len(suggestions), 3)
        for suggestion in suggestions:
            self.assertIn("主題", suggestion)
            self.assertIn("建議", suggestion)
            self.assertIn("模式", suggestion)
            self.assertIsInstance(suggestion["建議"], str)
            self.assertIsInstance(suggestion["模式"], str)

    def test_low_sentiment_score(self):
        topics = [{"topic": "法規與風險", "cluster": 3, "keywords": ["法規", "風險"]}]
        sentiment_counts = {"正向": 1, "中立": 2, "負向": 7}
        sentiment_avg = 0.32

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)
        self.assertEqual(suggestions[0]["模式"], "顧問服務 / B2B 解決方案")

    def test_high_sentiment_score(self):
        topics = [{"topic": "創作者經濟", "cluster": 4, "keywords": ["創作者", "經濟"]}]
        sentiment_counts = {"正向": 10, "中立": 0, "負向": 0}
        sentiment_avg = 0.82

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)
        self.assertEqual(suggestions[0]["模式"], "訂閱制 / 內容付費")

    def test_generate_suggestions_low_avg_no_negative_keywords(self):
        topics = [{"topic": "市場反應", "cluster": 5, "keywords": ["市場", "調查", "趨勢"]}]
        sentiment_counts = {"正向": 2, "中立": 3, "負向": 10}
        sentiment_avg = 0.25  # 整體偏負向

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)

        # 應該會 fallback 到整體情緒的建議
        self.assertEqual(suggestions[0]["主題"], "整體情緒")
        self.assertEqual(suggestions[0]["模式"], "顧問服務 / B2B 解決方案")

class TestSuggestionModuleExtended(unittest.TestCase):

    def test_no_topics(self):
        sentiment_counts = {"正向": 5, "中立": 2, "負向": 1}
        sentiment_avg = 0.7
        suggestions = generate_business_suggestions([], sentiment_counts, sentiment_avg)

        # 預期回傳 "整體情緒" 建議
        self.assertEqual(suggestions[0]["主題"], "整體情緒")
        self.assertEqual(suggestions[0]["模式"], "訂閱制 / 內容付費")

    def test_no_negative_sentiment(self):
        topics = [{"topic": "AI發展", "cluster": 1, "keywords": ["AI", "發展"]}]
        sentiment_counts = {"正向": 10, "中立": 0, "負向": 0}
        sentiment_avg = 0.85
        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)
        self.assertTrue(any(s["模式"] == "訂閱制 / 內容付費" for s in suggestions))
    def test_generate_suggestions_negative_keywords(self):
        topics = [{"topic": "用戶負評問題", "cluster": 6, "keywords": ["負評", "抱怨", "問題"]}]
        sentiment_counts = {"正向": 2, "中立": 3, "負向": 10}
        sentiment_avg = 0.3

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)
        assert suggestions[0]["模式"] in ["顧問服務 / B2B 解決方案", "客服改善 / 危機處理"]

    def test_generate_suggestions_no_topics_negative_sentiment(self):
        sentiment_counts = {"正向": 0, "中立": 2, "負向": 8}
        sentiment_avg = 0.2

        suggestions = generate_business_suggestions([], sentiment_counts, sentiment_avg)
        assert len(suggestions) >= 1
        主題_list = [s["主題"] for s in suggestions]
        assert "整體情緒" in 主題_list
        assert "品牌負評" in 主題_list
    
    def test_generate_suggestions_complaint_keyword(self):
        topics = [{"topic": "售後服務投訴", "cluster": 7, "keywords": ["售後", "服務", "投訴"]}]
        sentiment_counts = {"正向": 1, "中立": 2, "負向": 5}
        sentiment_avg = 0.4

        suggestions = generate_business_suggestions(topics, sentiment_counts, sentiment_avg)

        # 確認有針對 Cluster 投訴給出客戶服務優化建議
        cluster_suggestions = [s for s in suggestions if "Cluster 7" in s["主題"]]
        self.assertTrue(len(cluster_suggestions) > 0)
        self.assertEqual(cluster_suggestions[0]["模式"], "客戶服務優化")


if __name__ == '__main__':
    unittest.main()
