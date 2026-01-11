from services.gemini_client import GeminiClient
from config.prompts import REPORT_GENERATION_PROMPT
import json
import re

class ReportPipeline:
    def __init__(self):
        self.gemini_client = GeminiClient()

    def generate_report(self, brand, company_goal, stats):
        # Format top topics for the prompt
        top_topics_str = ", ".join([f"{t[0]} ({t[1]})" for t in stats['top_topics']])
        
        prompt = REPORT_GENERATION_PROMPT.format(
            brand=brand,
            goal=company_goal,
            avg_sentiment=stats['avg_sentiment'],
            negative_ratio=stats['negative_ratio'],
            top_topics=top_topics_str
        )
        
        response_text = self.gemini_client.generate_content(prompt)
        
        # Return raw markdown
        return {"report_markdown": response_text}

        
    def calculate_brand_health(self, avg_sentiment, negative_ratio):
        # normalize avg_sentiment (-1 to 1) to (0 to 1) -> (avg + 1) / 2
        # But user formula: 100 - (neg_ratio * 60) + (avg * 40)
        # Avg is between -1 and 1. 
        # If avg is -1, contribution is -40. If neg_ratio is 1, contribution is -60. Total 0.
        # If avg is 1, contribution 40. neg_ratio 0, -0. Total 140? 
        # Let's check max score: 100 - 0 + 40 = 140.
        # Max should be 100.
        # User formula: score = 100 - (neg_ratio * 60) + (avg * 40)
        # Let's cap it at 100, min 0.
        
        score = 100 - (negative_ratio * 60) + (avg_sentiment * 40)
        return max(0, min(100, int(score)))

    def run(self, brand, goal, stats):
        report = self.generate_report(brand, goal, stats)
        brand_health = self.calculate_brand_health(stats['avg_sentiment'], stats['negative_ratio'])
        
        final_output = {
            "brand_health_score": brand_health,
            "report_markdown": report.get("report_markdown", ""),
            "sentiment_overview": {
                "average_score": round(stats['avg_sentiment'], 3),
                "negative_ratio": round(stats['negative_ratio'], 3)
            }
        }
        return final_output
        return final_output
