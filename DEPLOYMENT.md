# Deployment Instructions

This guide explains how to run the Sentiment Intelligence System web app locally and how to share it effectively.

## 1. Local Development (Quick Start)

### Prerequisites
Ensure you have the dependencies installed:
```bash
pip install -r requirements.txt
```
*Note: You may need system libraries for PDF generation if you encounter errors (e.g., `libssl-dev`, `libffi-dev`).*

### Running the App
Run the following command in the project root:
```bash
streamlit run app.py
```
This will open the app in your browser at `http://localhost:8501`.

---

## 2. Public Sharing via ngrok (Easiest Method)

If you want to share your locally running app with someone else instantly without deploying to a cloud server:

1.  **Install ngrok**: [Download and install ngrok](https://ngrok.com/download).
2.  **Start the app**:
    ```bash
    streamlit run app.py
    ```
3.  **Start ngrok tunnel** (in a new terminal):
    ```bash
    ngrok http 8501
    ```
4.  Copy the `https://....ngrok-free.app` link and share it!

---

## 3. Deployment to Streamlit Cloud (Permanent)

For a permanent, always-online version:

1.  **Push your code to GitHub** (you have already done this!).
2.  **Sign up** for [Streamlit Cloud](https://streamlit.io/cloud).
3.  **New App**:
    - Connect your GitHub account.
    - Select your repository (`selmanimdat/nlp_report_maker`).
    - Set **Main file path** to `app.py`.
4.  **Secrets (Environment Variables)**:
    - Go to "Advanced Settings" during deployment.
    - Add your API keys from your `.env` file into the "Secrets" box in TOML format:
      ```toml
      GEMINI_API_KEY = "your-api-key-here"
      ```
    - *Note:* Streamlit Cloud handles `.env` variables via this Secrets manager.

5.  **Click Deploy!** 🚀

### A Note on Web Scraping in Cloud
Streamlit Cloud and other free hosting services (data centers) are often blocked by scraping targets like Şikayetvar.
- **If scraping fails on Cloud:** Users should use the "Upload JSON" feature instead, or you might need to use a proxy service for the scraper.
