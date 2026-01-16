from playwright.sync_api import sync_playwright
import os
import urllib.parse

def analyze_html_playwright():
    file_path = "/home/selman/Desktop/nlp ders/web scraping /Türk Telekom - Şikayetvar.html"
    
    # helper to handle spaces in path for file:// url
    abs_path = os.path.abspath(file_path)
    # properly encode the path
    url = "file://" + urllib.parse.quote(abs_path)
    
    # Handle the case where urllib might not encode everything like browsers do, 
    # but playwright handles file paths well if we just give it the path? 
    # Actually page.goto("file://...") works.
    
    print(f"Target URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")
            
            # Selector: article.card-v2
            cards = page.query_selector_all("article.card-v2")
            print(f"Found {len(cards)} cards.")

            if not cards:
                print("No cards found. Selector 'article.card-v2' might be wrong.")
            else:
                for i, card in enumerate(cards[:3]): 
                    print(f"\n--- Card {i+1} ---")
                    
                    # Selector: .complaint-description
                    desc = card.query_selector(".complaint-description")
                    if desc:
                        print(f"Description found: {desc.text_content().strip()[:50]}...")
                    else:
                        print("Description NOT found ('.complaint-description')")

                    # Selector: span.username
                    user = card.query_selector("span.username")
                    if user:
                         print(f"User found: {user.text_content().strip()}")
                    else:
                        print("User NOT found ('span.username')")

                    # Selector: .post-time .time
                    date_el = card.query_selector(".post-time .time")
                    if date_el:
                         print(f"Date found: {date_el.text_content().strip()}")
                    else:
                        print("Date NOT found ('.post-time .time')")
                        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    analyze_html_playwright()
