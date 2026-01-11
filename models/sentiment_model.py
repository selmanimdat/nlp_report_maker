from transformers import pipeline
import yaml
import os

# Load config
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

SENTIMENT_MODEL_NAME = config['sentiment']['model_name']

class SentimentModel:
    def __init__(self):
        print(f"Loading sentiment model: {SENTIMENT_MODEL_NAME}...")
        self.pipeline = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL_NAME,
            tokenizer=SENTIMENT_MODEL_NAME
        )
        self.label_map = {
            "negative": -1.0,
            "neutral": 0.0,
            "positive": 1.0,
            "LABEL_0": -1.0, # some models use LABEL_0/1/2
            "LABEL_1": 0.0,
            "LABEL_2": 1.0
        }

    def analyze(self, text):
        # Truncate if too long, though bert handles 512 tokens usually
        result = self.pipeline(text[:512])[0]
        label = result['label'].lower()
        
        # Mapping for the specific Turkish model 'savasy/bert-base-turkish-sentiment-cased'
        # It typically returns 'positive', 'negative', 'neutral'? 
        # Let's handle standard labels.
        # Check if label is in map, otherwise default to 0
        sentiment_val = self.label_map.get(label, 0.0)
        
        score = sentiment_val * result['score']
        return {
            "label": label,
            "score": round(score, 3),
            "confidence": round(result['score'], 3)
        }
