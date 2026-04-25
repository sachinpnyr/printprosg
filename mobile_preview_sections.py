from playwright.sync_api import sync_playwright
import os

OUT = "/home/ubuntu/printprosg/mobile_preview"
os.makedirs(OUT, exist_ok=True)

sections = [
    ("hero",        "#hero",        "01_hero.png"),
    ("reviews",     "#reviews",     "02_reviews.png"),
    ("about",       "#about",       "03_about.png"),
    ("how_it_works","#how-it-works","04_how_it_works.png"),
    ("services",    "#services",    "05_services.png"),
    ("portfolio",   "#portfolio",   "06_portfolio.png"),
    ("clients",     "#clients",     "07_clients.png"),
    ("locations",   "#locations",   "08_locations.png"),
    ("faq",         "#faq",         "09_faq.png"),
    ("contact",     "#contact",     "10_contact.png"),
    ("footer",      "footer",       "11_footer.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("file:///home/ubuntu/printprosg/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Full page screenshot
    page.screenshot(path=f"{OUT}/00_full_page.png", full_page=True)
    print("Full page saved")

    # Per-section screenshots
    for name, selector, filename in sections:
        try:
            el = page.query_selector(selector)
            if el:
                el.screenshot(path=f"{OUT}/{filename}")
                box = el.bounding_box()
                h = box["height"] if box else 0
                print(f"  {name}: {h:.0f}px → {filename}")
            else:
                print(f"  {name}: NOT FOUND")
        except Exception as e:
            print(f"  {name}: ERROR - {e}")

    browser.close()
    print("Done!")
