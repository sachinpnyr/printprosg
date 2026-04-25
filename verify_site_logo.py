from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    
    # Screenshot navbar
    nav = page.query_selector('nav') or page.query_selector('.navbar') or page.query_selector('header')
    if nav:
        nav.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/navbar_logo.png')
        print("Navbar screenshot saved")
    
    # Screenshot footer
    footer = page.query_selector('footer') or page.query_selector('.footer')
    if footer:
        footer.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/footer_logo.png')
        print("Footer screenshot saved")
    
    browser.close()
