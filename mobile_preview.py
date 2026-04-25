from playwright.sync_api import sync_playwright
import os

os.makedirs('/home/ubuntu/printprosg/mobile_preview', exist_ok=True)

sections = [
    ('navbar',      0),
    ('hero',        200),
    ('reviews',     1200),
    ('about',       2000),
    ('how_it_works',2700),
    ('services',    3400),
    ('portfolio',   4300),
    ('locations',   5100),
    ('faq',         5700),
    ('contact',     6300),
    ('footer',      7000),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    # iPhone 14 Pro dimensions
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('https://8090-irj92ex2x0b9r8yzz0s0h-f37a8bc9.sg1.manus.computer', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Full page screenshot
    page.screenshot(path='/home/ubuntu/printprosg/mobile_preview/full_mobile.png', full_page=True)
    print("Full page screenshot saved")

    # Section screenshots
    for name, scroll_y in sections:
        page.evaluate(f'window.scrollTo(0, {scroll_y})')
        page.wait_for_timeout(400)
        page.screenshot(path=f'/home/ubuntu/printprosg/mobile_preview/{name}.png')
        print(f"  {name} @ y={scroll_y}")

    browser.close()
    print("Done.")
