from playwright.sync_api import sync_playwright
import time, os

OUT = "/home/ubuntu/printprosg/screenshots_v51"
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for w, h, label in [(390, 844, "mobile"), (768, 1024, "tablet"), (1440, 900, "desktop")]:
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.goto('http://localhost:8090/', wait_until='networkidle')
        time.sleep(2)
        path = f"{OUT}/final_{label}_{w}.png"
        page.screenshot(path=path, full_page=True)
        total_h = page.evaluate('document.body.scrollHeight')
        print(f"{label} ({w}px): {total_h}px -> {path}")
        page.close()
    
    browser.close()
print("Done!")
