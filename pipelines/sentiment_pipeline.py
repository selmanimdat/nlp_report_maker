from models.sentiment_model import SentimentModel
from services.gemini_client import GeminiClient
from config.prompts import TOPIC_EXTRACTION_PROMPT

class SentimentPipeline:
    def __init__(self):
        self.sentiment_model = SentimentModel()
        self.gemini_client = GeminiClient()

    def process_comment(self, comment):
        # 1. Sentiment Analysis
        sentiment = self.sentiment_model.analyze(comment['text'])
        
        # 2. Topic Extraction (using Gemini)
        topic_prompt = TOPIC_EXTRACTION_PROMPT.format(comment=comment['text'])
        topic = self.gemini_client.generate_content(topic_prompt).strip().lower()
        
        # Clean up topic (remove extra quotes or newlines if any)
        topic = topic.replace('"', '').replace("'", "").split('\n')[0]

        return {
            "id": comment['id'],
            "text": comment['text'],
            "sentiment": sentiment,
            "topic": topic,
            "platform": comment.get('platform'),
            "date": comment.get('date')
        }

    def run(self, comments):
        processed_comments = []
        print(f"Processing {len(comments)} comments...")
        for comment in comments:
            processed = self.process_comment(comment)
            processed_comments.append(processed)
        return processed_comments
