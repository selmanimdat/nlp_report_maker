from playwright.sync_api import sync_playwright
import json
import time
import argparse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def scrape_sikayetvar(company_slug, max_items=100, output_file="data.json"):
    url = f"https://www.sikayetvar.com/{company_slug}"
    data = []
    
    logger.info(f"Starting scrape for company: {company_slug}, Target items: {max_items}")

    with sync_playwright() as p:
        logger.info("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36"
        )
        page = context.new_page()

        logger.info(f"Navigating to {url}...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            browser.close()
            return []

        # 🔴 KRİTİK: JS'in ilk batch'i basması için bekle
        time.sleep(5)

        # 🔴 KRİTİK: ilk scroll olmadan kartlar gelmiyor
        logger.info("Performing initial scroll...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        prev_len = 0
        stagnation = 0

        while len(data) < max_items and stagnation < 3:
            cards = page.query_selector_all("article.card-v2")
            
            # Log progress every batch or if stagnant
            if len(cards) == prev_len:
                stagnation += 1
                logger.debug(f"Stagnation detected ({stagnation}/3). Card count: {len(cards)}")
            else:
                stagnation = 0
                logger.info(f"Found {len(cards)} cards so far...")

            prev_len = len(cards)

            # Process new cards
            new_cards_indices = range(len(data), len(cards))
            
            for i in new_cards_indices:
                if len(data) >= max_items:
                    break
                
                card = cards[i]
                try:
                    desc = card.query_selector(".complaint-description")
                    if not desc:
                        continue

                    text = desc.text_content().strip()
                    if not text:
                        continue

                    user = card.query_selector("span.username")
                    date = card.query_selector(".post-time .time")

                    data.append({
                        "company": company_slug,
                        "text": text,
                        "user": user.text_content().strip() if user else None,
                        "date": date.text_content().strip() if date else None
                    })

                except Exception as e:
                    logger.warning(f"Error processing card: {e}")
                    continue

            # Check if we are done before scrolling again
            if len(data) >= max_items:
                break

            # yeni batch tetikle
            page.keyboard.press("End")
            time.sleep(3)

        browser.close()
        logger.info("Browser closed.")

    logger.info(f"Scraping completed. Collected {len(data)} items.")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Data saved to {output_file}")

    return data

def main():
    parser = argparse.ArgumentParser(description="Scrape complaints from Sikayetvar.")
    parser.add_argument("--company", type=str, default="turk-telekom", help="Company slug to scrape (default: turk-telekom)")
    parser.add_argument("--max", type=int, default=100, help="Maximum number of items to scrape (default: 100)")
    parser.add_argument("--output", type=str, default="data.json", help="Output JSON file path (default: data.json)")
    
    args = parser.parse_args()
    
    data = scrape_sikayetvar(
        company_slug=args.company,
        max_items=args.max,
        output_file=args.output
    )
    
    print(len(data))

if __name__ == "__main__":
    main()
