from playwright.sync_api import sync_playwright
import os

os.makedirs("/home/ubuntu/printprosg/premium_final", exist_ok=True)

sections = [
    ("hero", "#hero"),
    ("about", "#about"),
    ("how_it_works", "#how-it-works"),
    ("services", "#services"),
    ("portfolio", "#portfolio"),
    ("reviews", "#reviews"),
    ("faq", "#faq"),
    ("contact", "#contact"),
    ("footer", "footer"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://localhost:9090/index.html", wait_until="networkidle")
    page.wait_for_timeout(3000)

    for name, selector in sections:
        try:
            el = page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(600)
                el.screenshot(path=f"/home/ubuntu/printprosg/premium_final/{name}.png")
                print(f"✓ {name}")
            else:
                print(f"✗ {name} — selector not found")
        except Exception as e:
            print(f"✗ {name} — {e}")

    # Full page
    page.goto("http://localhost:9090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.screenshot(path="/home/ubuntu/printprosg/premium_final/full_page.png", full_page=True)
    print("✓ full_page")

    browser.close()
    print("Done.")
