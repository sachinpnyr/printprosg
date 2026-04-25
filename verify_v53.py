from playwright.sync_api import sync_playwright
import os

os.makedirs('/home/ubuntu/printprosg/v53_verify', exist_ok=True)

sections = [
    ('navbar', '#navbar', 0),
    ('hero', '#hero', 0),
    ('reviews', '#reviews', 0),
    ('about', '#about', 0),
    ('how_it_works', '#how-it-works', 0),
    ('services', '#services', 0),
    ('portfolio', '#portfolio', 0),
    ('clients', '#clients', 0),
    ('locations', '#locations', 0),
    ('faq', '#faq', 0),
    ('contact', '#contact', 0),
    ('footer', 'footer', 0),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Dismiss cookie banner
    try:
        page.click('#cookie-accept', timeout=2000)
        page.wait_for_timeout(300)
    except:
        pass

    # Full page screenshot
    page.screenshot(path='/home/ubuntu/printprosg/v53_verify/00_full_mobile.png', full_page=True)
    print("Full page screenshot taken")

    # Section screenshots
    for name, selector, extra_scroll in sections:
        try:
            el = page.query_selector(selector)
            if el:
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(400)
                box = el.bounding_box()
                if box:
                    # Take a viewport-height screenshot from the section start
                    clip_y = max(0, box['y'])
                    clip_h = min(844, box['height'])
                    page.screenshot(
                        path=f'/home/ubuntu/printprosg/v53_verify/{name}.png',
                        clip={'x': 0, 'y': clip_y, 'width': 390, 'height': clip_h}
                    )
                    print(f"  {name}: y={clip_y:.0f}, h={box['height']:.0f}px")
        except Exception as e:
            print(f"  {name}: ERROR - {e}")

    # Measure section heights
    print("\n=== SECTION HEIGHTS ===")
    total = 0
    for name, selector, _ in sections:
        el = page.query_selector(selector)
        if el:
            box = el.bounding_box()
            if box:
                print(f"  {name}: {box['height']:.0f}px")
                total += box['height']
    print(f"  TOTAL: {total:.0f}px")

    # Measure navbar height specifically
    nav = page.query_selector('#navbar')
    if nav:
        box = nav.bounding_box()
        print(f"\nNavbar total height: {box['height']:.0f}px")

    browser.close()
    print("\nDone!")
