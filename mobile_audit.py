"""
Mobile audit script — screenshots every section at 390×844 (iPhone 15 Pro)
Saves to /tmp/mob_<section>.png
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io

SECTIONS = [
    "hero", "products", "reviews", "design-services",
    "about", "how-it-works", "services", "portfolio",
    "clients", "blog", "locations", "faq", "contact", "footer"
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    # iPhone 15 Pro viewport
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    )
    page.goto("http://localhost:8090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Scroll through entire page to trigger lazy loading
    total_height = page.evaluate("document.body.scrollHeight")
    current = 0
    while current < total_height:
        page.evaluate(f"window.scrollTo(0, {current})")
        page.wait_for_timeout(150)
        current += 400

    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)

    # Force all reveals visible
    page.evaluate("""
        document.querySelectorAll('.reveal').forEach(el => {
            el.classList.add('visible');
            el.style.opacity = '1';
            el.style.transform = 'none';
        });
    """)
    page.wait_for_timeout(300)

    # Full page screenshot
    screenshot = page.screenshot(full_page=True)
    img = Image.open(io.BytesIO(screenshot))
    img.save('/tmp/mob_full.png')
    print(f"Full page: {img.size[0]}x{img.size[1]}px")

    # Per-section screenshots
    for section_id in SECTIONS:
        el = page.query_selector(f"#{section_id}")
        if el:
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            screenshot = page.screenshot()
            sec_img = Image.open(io.BytesIO(screenshot))
            sec_img.save(f'/tmp/mob_{section_id}.png')
            print(f"  #{section_id} ✓  ({sec_img.size[0]}x{sec_img.size[1]})")
        else:
            print(f"  #{section_id} NOT FOUND")

    browser.close()
    print("Audit complete.")
