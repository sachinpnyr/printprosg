from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    
    # Scroll to footer
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    
    # Screenshot the footer brand section specifically
    footer_brand = page.query_selector('.footer-brand')
    if footer_brand:
        footer_brand.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/footer_brand_logo.png')
        print("Footer brand screenshot saved")
    
    # Also screenshot the full footer
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/footer_bottom.png', clip={
        'x': 0,
        'y': page.evaluate("document.body.scrollHeight - 844"),
        'width': 390,
        'height': 844
    })
    print("Footer bottom screenshot saved")
    
    browser.close()
