"""
Mobile verification screenshots for PrintProSG v51
Takes full-page screenshot + individual section screenshots at 390px
"""
from playwright.sync_api import sync_playwright
import os, time

OUTPUT_DIR = "/home/ubuntu/printprosg/screenshots_v51"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SECTIONS = ["hero", "reviews", "about", "how-it-works", "services", 
            "portfolio", "clients", "locations", "faq", "contact"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Mobile 390px
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    
    # Full page screenshot
    page.screenshot(path=f"{OUTPUT_DIR}/full_mobile_390.png", full_page=True)
    print(f"Full page: {page.evaluate('document.body.scrollHeight')}px")
    
    # Individual section screenshots
    for section_id in SECTIONS:
        el = page.query_selector(f"#{section_id}")
        if el:
            h = el.evaluate("el => el.offsetHeight")
            el.screenshot(path=f"{OUTPUT_DIR}/{section_id}_390.png")
            print(f"  #{section_id}: {h}px -> screenshot saved")
        else:
            print(f"  #{section_id}: NOT FOUND")
    
    # Tablet 768px
    page2 = browser.new_page(viewport={'width': 768, 'height': 1024})
    page2.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    page2.screenshot(path=f"{OUTPUT_DIR}/full_tablet_768.png", full_page=True)
    print(f"\nTablet 768px: {page2.evaluate('document.body.scrollHeight')}px")
    
    # Desktop 1440px
    page3 = browser.new_page(viewport={'width': 1440, 'height': 900})
    page3.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    page3.screenshot(path=f"{OUTPUT_DIR}/full_desktop_1440.png", full_page=True)
    print(f"Desktop 1440px: {page3.evaluate('document.body.scrollHeight')}px")
    
    browser.close()

print(f"\nAll screenshots saved to {OUTPUT_DIR}/")
