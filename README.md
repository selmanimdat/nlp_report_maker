# Sentiment Intelligence System

A comprehensive sentiment analysis and reporting tool that uses BERT for sentiment classification and Google Gemini (LLM) for generating detailed, strategic business reports.

## Features
- **Sentiment Analysis**: Uses `savasy/bert-base-turkish-sentiment-cased` for accurate Turkish sentiment detection.
- **Topic Extraction**: Identifies key topics from customer comments.
- **Smart Reporting**: Generates a 1-2 page professional Markdown report with executive summary, critical issues, and strategic recommendations using Gemini 2.0 Flash.
- **Data Aggregation**: Calculates sentiment scores and negative feedback ratios.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sentiment-intelligence
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   - Create a `.env` file in the root directory.
   - Add your Google Gemini API key:
     ```env
     GEMINI_API_KEY="your_api_key_here"
     ```

## Usage

1. **Prepare Input Data:**
   - Ensure your data is in `schemas/input_schema.json` format.

2. **Run the Analysis:**
   ```bash
   python main.py
   ```

3. **View Results:**
   - **`report.md`**: The detailed, professionally formatted insight report.
   - **`output.json`**: Raw statistics and data.

## Project Structure
- `pipelines/`: Core logic for sentiment, aggregation, and reporting.
- `models/`: Model management.
- `config/`: Configuration settings and prompts.
- `schemas/`: Input/Output data definitions.
