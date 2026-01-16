import os
import sys
import subprocess
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_scraper(company, max_items, output_file):
    """
    Runs the web scraper script located in 'web scraping /main.py'.
    Attempts to use the venv inside 'web scraping ' if it exists.
    """
    scraper_dir = os.path.join(os.getcwd(), "web scraping ")
    scraper_script = os.path.join(scraper_dir, "main.py")
    
    # Check for scraper venv
    scraper_venv_python = os.path.join(scraper_dir, ".venv", "bin", "python")
    if os.path.exists(scraper_venv_python):
        python_executable = scraper_venv_python
        logger.info(f"Using scraper venv: {python_executable}")
    else:
        python_executable = sys.executable
        logger.info(f"Using system python: {python_executable}")
        
    cmd = [
        python_executable,
        scraper_script,
        "--company", company,
        "--max", str(max_items),
        "--output", output_file
    ]
    
    logger.info(f"Running scraper command: {' '.join(cmd)}")
    
    try:
        # Run scraper process
        # We set cwd to scraper dir because it might rely on relative paths (like chromedriver or logs)
        subprocess.run(cmd, check=True, cwd=scraper_dir)
        logger.info("Scraping completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Scraper failed with exit code {e.returncode}")
        return False
    except Exception as e:
        logger.error(f"Error running scraper: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Full Sentiment Intelligence Pipeline")
    parser.add_argument("--company", required=True, help="Company slug to scrape (e.g., 'turk-telekom')")
    parser.add_argument("--max", type=int, default=10, help="Max items to scrape")
    args = parser.parse_args()
    
    # 1. Scrape Data
    logger.info(">>> STEP 1: Starting Web Scraping...")
    # We'll save the scraped data to a temporary location or just straight to the web scraping dir
    scraped_file_name = f"{args.company}_latest.json"
    # Note: The scraper script saves relative to its CWD.
    
    if not run_scraper(args.company, args.max, scraped_file_name):
        logger.error("Aborting pipeline due to scraper failure.")
        return

    # The file should now exist in 'web scraping /' directory
    scraped_file_path = os.path.join("web scraping ", scraped_file_name)
    
    if not os.path.exists(scraped_file_path):
        logger.error(f"Expected scraped file not found at {scraped_file_path}")
        return

    # 2. Run Analysis Pipeline
    logger.info(">>> STEP 2: Starting Sentiment Analysis Pipeline...")
    
    # Import main module dynamically to avoid running it on import (though we fixed that)
    # But running it via function call is cleaner
    try:
        from main import main as run_analysis
        
        # Prepare arguments for the main pipeline
        analysis_args = [
            "--scraped-data", scraped_file_path,
            "--output", f"{args.company}_report.json"
        ]
        
        run_analysis(analysis_args)
        logger.info(">>> Pipeline completed successfully.")
        
    except ImportError:
        logger.error("Could not import main pipeline script.")
    except Exception as e:
        logger.error(f"Error during analysis pipeline: {e}")

if __name__ == "__main__":
    main()
