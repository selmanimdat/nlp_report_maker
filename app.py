import streamlit as st
import pandas as pd
import json
import os
import shutil
import tempfile
import logging
from full_pipeline import run_scraper
from services.data_loader import load_scraped_data
from pipelines.sentiment_pipeline import SentimentPipeline
from pipelines.aggregation_pipeline import AggregationPipeline
from pipelines.report_pipeline import ReportPipeline
from fpdf import FPDF
import re

# ... (logging setup is same) ...

# --- PDF Generation Utility ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sentiment Intelligence Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(report_content, stats):
    """
    Converts markdown report and stats to PDF using FPDF.
    """
    pdf = PDF()
    pdf.add_page()
    
    # 1. Stats Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Key Metrics', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"Average Sentiment: {stats['avg_sentiment']:.3f}", 0, 1)
    pdf.cell(0, 7, f"Negative Ratio: {stats['negative_ratio']:.2f}", 0, 1)
    pdf.ln(5)
    
    # 2. Report Content
    # Simple markdown stripping for cleaner text
    pdf.set_font('Arial', '', 11)
    
    # Remove #, *, etc for cleaner plain text
    lines = report_content.split('\n')
    for line in lines:
        clean_line = line.strip()
        # Header handling
        if clean_line.startswith('#'):
            clean_line = clean_line.lstrip('#').strip()
            pdf.set_font('Arial', 'B', 12)
            pdf.ln(2)
            pdf.multi_cell(0, 7, clean_line)
            pdf.set_font('Arial', '', 11)
        else:
            # Bold cleanup
            clean_line = clean_line.replace('**', '').replace('__', '')
            if clean_line:
                pdf.multi_cell(0, 6, clean_line)
                
    pdf_file = tempfile.mktemp(suffix=".pdf")
    pdf.output(pdf_file, 'F')
    return pdf_file

# --- UI Layout ---

st.title("🤖 Sentiment Intelligence System")
st.markdown("Analyze customer sentiment from Şikayetvar and other sources using Gemini AI.")

# --- Sidebar ---
st.sidebar.header("Configuration")
mode = st.sidebar.radio("Input Source", ["Live Scraping (Şikayetvar)", "Upload JSON"])

scraped_file_path = None

if mode == "Live Scraping (Şikayetvar)":
    company_slug = st.sidebar.text_input("Company Slug", value="turk-telekom", help="e.g., turk-telekom, garanti-bbva")
    max_items = st.sidebar.number_input("Max Comments", min_value=1, max_value=100, value=10)
    
    if st.sidebar.button("Fetch Data & Analyze", type="primary"):
        with st.spinner(f"Scraping {max_items} comments for '{company_slug}'..."):
            output_filename = f"{company_slug}_latest_web.json"
            # We assume run_scraper saves to 'web scraping /<filename>' as per full_pipeline logic
            # full_pipeline.run_scraper expects output_file argument
            
            # Since run_scraper saves to the scraping dir, we need to respect that
            scraper_dir = os.path.join(os.getcwd(), "web scraping ")
            target_path = os.path.join(scraper_dir, output_filename)
            
            success = run_scraper(company_slug, max_items, output_filename)
            
            if success:
                st.success("✅ Scraping completed!")
                scraped_file_path = target_path
            else:
                st.error("❌ Scraping failed. Check logs.")

elif mode == "Upload JSON":
    uploaded_file = st.sidebar.file_uploader("Upload scraped JSON", type=["json"])
    if uploaded_file:
        # Save temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
            tmp.write(uploaded_file.getvalue())
            scraped_file_path = tmp.name
        st.sidebar.success("File uploaded!")

# --- Analysis Pipeline ---

if scraped_file_path and os.path.exists(scraped_file_path):
    st.divider()
    
    # 1. Load Data
    st.subheader("1. Data Preview")
    
    # Use our data loader service
    loaded_data = load_scraped_data(scraped_file_path)
    if not loaded_data:
        st.error("Failed to load data.")
        st.stop()
        
    comments = loaded_data.get("comments", [])
    brand = loaded_data.get("brand", "Unknown")
    
    if not comments:
        st.warning("No comments found in the file.")
        st.stop()
        
    # Show dataframe
    df = pd.DataFrame(comments)
    st.dataframe(df[["date", "platform", "text"]], use_container_width=True)
    
    st.info(f"Loaded {len(comments)} comments for brand: **{brand}**")

    # 2. Run Pipeline
    if st.button("Run AI Analysis") or mode == "Live Scraping (Şikayetvar)": # Auto run if scraping just finished
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Sentiment Analysis
            status_text.text("Running Sentiment Analysis (BERT)...")
            sentiment_pipeline = SentimentPipeline()
            processed_comments = sentiment_pipeline.run(comments)
            progress_bar.progress(40)
            
            # Step 2: Aggregation
            status_text.text("Aggregating Statistics...")
            agg_pipeline = AggregationPipeline()
            stats = agg_pipeline.run(processed_comments)
            progress_bar.progress(70)
            
            # Step 3: Report Gen
            status_text.text("Genering Gemini Report...")
            report_pipeline = ReportPipeline()
            
            # Default goal
            goal = "Genel müşteri memnuniyeti analizi"
            final_report = report_pipeline.run(brand, goal, stats)
            progress_bar.progress(100)
            status_text.text("Analysis Complete!")
            
            # --- Results Display ---
            st.divider()
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            col1.metric("Brand Health Score", f"{final_report['brand_health_score']}/100")
            col2.metric("Avg Sentiment", f"{stats['avg_sentiment']:.2f}")
            col3.metric("Negative Ratio", f"{stats['negative_ratio']:.0%}")
            
            # Report
            st.subheader("📝 AI Executive Report")
            report_md = final_report.get("report_markdown", "")
            if report_md:
                st.markdown(report_md)
                
                # PDF Export
                st.subheader("Download Report")
                pdf_path = create_pdf(report_md, stats)
                if pdf_path:
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📄 Download Report as PDF",
                            data=pdf_file,
                            file_name=f"{brand}_sentiment_report.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.warning("Could not generate PDF.")
            else:
                st.warning("Report generation returned empty content (possibly API quota).")
                
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
            logger.error(f"Pipeline error: {e}", exc_info=True)
            
