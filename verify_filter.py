from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)

    # Scroll to services section
    page.evaluate("document.getElementById('services').scrollIntoView()")
    time.sleep(1)

    # Screenshot: Most Popular (default)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/filter_most_popular.png',
                    clip={'x': 0, 'y': 0, 'width': 1440, 'height': 200})
    
    # Count visible cards
    visible = page.evaluate("""
        Array.from(document.querySelectorAll('#services-grid .service-card'))
             .filter(c => c.style.display !== 'none').length
    """)
    print(f"Most Popular: {visible} cards visible")

    # Click "Stickers"
    page.click('[data-filter="stickers"]')
    time.sleep(0.5)
    visible = page.evaluate("""
        Array.from(document.querySelectorAll('#services-grid .service-card'))
             .filter(c => c.style.display !== 'none').length
    """)
    print(f"Stickers: {visible} cards visible")

    # Click "Displays & Banners"
    page.click('[data-filter="displays"]')
    time.sleep(0.5)
    visible = page.evaluate("""
        Array.from(document.querySelectorAll('#services-grid .service-card'))
             .filter(c => c.style.display !== 'none').length
    """)
    print(f"Displays & Banners: {visible} cards visible")

    # Click "Promo & Giveaways"
    page.click('[data-filter="promo"]')
    time.sleep(0.5)
    visible = page.evaluate("""
        Array.from(document.querySelectorAll('#services-grid .service-card'))
             .filter(c => c.style.display !== 'none').length
    """)
    print(f"Promo & Giveaways: {visible} cards visible")

    # Screenshot the services section with Promo filter active
    page.evaluate("document.getElementById('services').scrollIntoView()")
    time.sleep(0.5)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/filter_promo.png')
    print("Screenshots saved")

    # Click back to Most Popular and screenshot
    page.click('[data-filter="most-popular"]')
    time.sleep(0.5)
    page.evaluate("document.getElementById('services').scrollIntoView()")
    time.sleep(0.5)
    page.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/filter_most_popular_full.png')

    browser.close()
