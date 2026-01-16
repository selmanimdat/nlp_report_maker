import google.generativeai as genai
import openai
import yaml
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Load config
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except Exception as e:
    logger.error(f"Failed to load settings.yaml: {e}")
    config = {"gemini": {}}

# Gemini Config
GEMINI_API_KEY = config.get('gemini', {}).get('api_key') or os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = config.get('gemini', {}).get('model_name', "gemini-pro")

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-4-turbo"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

class LLMService:
    def __init__(self):
        self.gemini_model = None
        if GEMINI_API_KEY:
             self.gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        
    def generate_content(self, prompt):
        """
        Generates content using OpenAI, falling back to Gemini if necessary.
        """
        # 1. Try OpenAI
        if OPENAI_API_KEY:
            try:
                logger.info("Attempting to generate content with OpenAI...")
                response = openai.chat.completions.create(
                    model=OPENAI_MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant generating reports."},
                        {"role": "user", "content": prompt}
                    ]
                )
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}. Switching to fallback...")
        else:
            logger.warning("OpenAI API Key not configured.")

        # 2. Fallback to Gemini
        if self.gemini_model:
            try:
                logger.info("Attempting to generate content with Gemini...")
                response = self.gemini_model.generate_content(prompt)
                if response.text:
                    return response.text
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")
        else:
            logger.warning("Gemini API Key not configured or fallback failed.")
            
        return ""
