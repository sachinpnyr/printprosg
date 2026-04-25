"""
Comprehensive QA screenshot script.
Captures every section at 3 viewports: 1440px (desktop), 768px (tablet), 390px (mobile).
Scrolls through the full page first to trigger lazy loading.
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, os

SECTIONS = [
    ("navbar",          "nav#navbar"),
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

VIEWPORTS = [
    ("desktop", 1440, 900, False),
    ("tablet",  768,  1024, True),
    ("mobile",  390,  844,  True),
]

def screenshot_viewport(page, label, width, height, is_mobile):
    page.set_viewport_size({"width": width, "height": height})
    page.goto("http://localhost:8090/index.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    # Scroll through entire page to trigger lazy loading
    total_height = page.evaluate("document.body.scrollHeight")
    scroll_step = 500
    current = 0
    while current < total_height:
        page.evaluate(f"window.scrollTo(0, {current})")
        page.wait_for_timeout(100)
        current += scroll_step

    # Force all reveals visible
    page.evaluate("""
        document.querySelectorAll('[class*="reveal"]').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'none';
            el.style.visibility = 'visible';
            el.classList.add('visible');
        });
    """)
    page.wait_for_timeout(500)

    # Scroll back to top
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)

    results = []
    for name, selector in SECTIONS:
        try:
            el = page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(400)
                img_bytes = page.screenshot()
                img = Image.open(io.BytesIO(img_bytes))
                out = f"/tmp/qa_{label}_{name}.png"
                img.save(out)
                results.append((name, True, out))
            else:
                results.append((name, False, "selector not found"))
        except Exception as e:
            results.append((name, False, str(e)))

    return results

with sync_playwright() as p:
    for label, width, height, is_mobile in VIEWPORTS:
        print(f"\n{'='*50}")
        print(f"  {label.upper()} ({width}x{height})")
        print(f"{'='*50}")

        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" if is_mobile else None
        browser = p.chromium.launch()
        ctx_args = {"viewport": {"width": width, "height": height}}
        if is_mobile:
            ctx_args["is_mobile"] = True
            ctx_args["device_scale_factor"] = 2
            ctx_args["user_agent"] = ua
        page = browser.new_page(**ctx_args)

        results = screenshot_viewport(page, label, width, height, is_mobile)
        for name, ok, info in results:
            status = "✓" if ok else "✗"
            print(f"  {status} {name}")

        browser.close()

print("\nAll screenshots saved to /tmp/qa_*.png")
