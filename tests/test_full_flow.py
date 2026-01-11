import sys
import os
import json
import unittest

# Add root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipelines.sentiment_pipeline import SentimentPipeline
from pipelines.aggregation_pipeline import AggregationPipeline
from pipelines.report_pipeline import ReportPipeline

class TestFlow(unittest.TestCase):
    def setUp(self):
        self.sample_comments = [
            {"id": 1, "text": "Ürün harika, çok beğendim.", "platform": "twitter"},
            {"id": 2, "text": "Kargo rezalet, asla tavsiye etmem.", "platform": "instagram"},
            {"id": 3, "text": "Fiyat performans ürünü, idare eder.", "platform": "trendyol"}
        ]
        self.brand = "Test Brand"
        self.goal = "Test Goal"

    def test_pipeline_flow(self):
        print("\n--- Testing Full Pipeline Flow ---")
        
        # 1. Sentiment
        print("1. Sentiment Pipeline")
        sp = SentimentPipeline()
        processed = sp.run(self.sample_comments)
        self.assertEqual(len(processed), 3)
        self.assertTrue("sentiment" in processed[0])
        self.assertTrue("topic" in processed[0])
        
        # Check sentiment values (approximate)
        # "Ürün harika" should be positive
        print(f"Comment 1 Sentiment: {processed[0]['sentiment']}")
        # "Kargo rezalet" should be negative
        print(f"Comment 2 Sentiment: {processed[1]['sentiment']}")

        # 2. Aggregation
        print("2. Aggregation Pipeline")
        ap = AggregationPipeline()
        stats = ap.run(processed)
        self.assertIn("avg_sentiment", stats)
        self.assertIn("negative_ratio", stats)
        print(f"Stats: {stats}")

        # 3. Report
        print("3. Report Pipeline")
        rp = ReportPipeline()
        # Mocking or running real if API key exists.
        # If no API key, it might fail or print warning.
        # This test assumes we might want to skip or handle gracefully if key is missing.
        
        report = rp.run(self.brand, self.goal, stats)
        print("Final Report Keys:", report.keys())
        self.assertIn("brand_health_score", report)
        self.assertIn("executive_summary", report)

if __name__ == "__main__":
    unittest.main()
