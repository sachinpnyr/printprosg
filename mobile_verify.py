"""
Mobile verification screenshots at 390px (iPhone 15 Pro)
Scrolls through the page to trigger lazy loading, then crops each section.
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, os

SECTIONS = [
    ("hero",            "#hero"),
    ("products",        "#products"),
    ("reviews",         "#reviews"),
    ("design_services", "#design-services"),
    ("about",           "#about"),
    ("how_it_works",    "#how-it-works"),
    ("services",        "#services"),
    ("portfolio",       "#portfolio"),
    ("clients",         "#clients"),
    ("blog",            "#blog"),
    ("locations",       "#locations"),
    ("faq",             "#faq"),
    ("contact",         "#contact"),
    ("footer",          "footer"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
    )
    page.goto("http://localhost:8090/index.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    # Scroll through entire page to trigger lazy loading
    total_height = page.evaluate("document.body.scrollHeight")
    scroll_step = 600
    current = 0
    while current < total_height:
        page.evaluate(f"window.scrollTo(0, {current})")
        page.wait_for_timeout(150)
        current += scroll_step

    # Force all reveals visible
    page.evaluate("""
        document.querySelectorAll('.reveal, .reveal-delay-1, .reveal-delay-2, .reveal-delay-3').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'none';
            el.style.visibility = 'visible';
            el.classList.add('visible');
        });
    """)
    page.wait_for_timeout(500)

    # Screenshot each section
    for name, selector in SECTIONS:
        try:
            el = page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(400)
                img_bytes = page.screenshot()
                img = Image.open(io.BytesIO(img_bytes))
                out = f"/tmp/mob50_{name}.png"
                img.save(out)
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} — selector not found")
        except Exception as e:
            print(f"  ✗ {name} — {e}")

    browser.close()
    print("Done.")
