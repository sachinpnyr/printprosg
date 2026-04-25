"""
Full-page screenshot with lazy loading triggered by scrolling.
Saves individual section screenshots for audit.
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, os

SECTIONS = [
    "hero", "products", "reviews", "design-services",
    "about", "how-it-works", "services", "portfolio",
    "clients", "blog", "locations", "faq", "contact", "footer"
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Scroll through entire page to trigger lazy loading
    total_height = page.evaluate("document.body.scrollHeight")
    scroll_step = 600
    current = 0
    while current < total_height:
        page.evaluate(f"window.scrollTo(0, {current})")
        page.wait_for_timeout(300)
        current += scroll_step

    # Scroll back to top
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
    page.wait_for_timeout(500)

    # Take full page screenshot
    screenshot = page.screenshot(full_page=True)
    img = Image.open(io.BytesIO(screenshot))
    img.save('/tmp/final_full_page.png')
    print(f"Full page saved: {img.size}")

    # Take section screenshots by scrolling to each
    for section_id in SECTIONS:
        el = page.query_selector(f"#{section_id}")
        if el:
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(800)
            screenshot = page.screenshot()
            sec_img = Image.open(io.BytesIO(screenshot))
            sec_img.save(f'/tmp/final_{section_id}.png')
            print(f"Section #{section_id} saved")
        else:
            print(f"Section #{section_id} NOT FOUND")

    browser.close()
    print("Done!")
