import google.generativeai as genai
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

# Load config
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

API_KEY = config['gemini'].get('api_key') or os.getenv("GEMINI_API_KEY")
MODEL_NAME = config['gemini']['model_name']

if not API_KEY:
    # Fallback or warning
    print("WARNING: Gemini API Key not found in settings or env vars.")

genai.configure(api_key=API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""
