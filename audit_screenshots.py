from playwright.sync_api import sync_playwright
import time, os

os.makedirs('/home/ubuntu/printprosg/audit', exist_ok=True)

SECTIONS = [
    ('announcement_bar', '#announcement-bar'),
    ('navbar', '#navbar'),
    ('hero', '#hero'),
    ('reviews', '#reviews'),
    ('about', '#about'),
    ('how_it_works', '#how-it-works'),
    ('services', '#services'),
    ('portfolio', '#portfolio'),
    ('clients', '#clients'),
    ('locations', '#locations'),
    ('faq', '#faq'),
    ('contact', '#contact'),
    ('footer', 'footer'),
]

VIEWPORTS = [
    ('desktop', 1440, 900),
    ('tablet', 768, 1024),
    ('mobile', 390, 844),
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for vp_name, w, h in VIEWPORTS:
        print(f"\n=== {vp_name.upper()} ({w}x{h}) ===")
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.goto('http://localhost:8090/', wait_until='networkidle')
        time.sleep(2)

        # Close announcement bar if present
        try:
            page.click('#close-announcement', timeout=2000)
            time.sleep(0.3)
        except:
            pass

        # Full page screenshot
        page.screenshot(
            path=f'/home/ubuntu/printprosg/audit/full_{vp_name}.png',
            full_page=True
        )
        print(f"  Full page saved")

        # Per-section screenshots
        for sec_name, selector in SECTIONS:
            try:
                el = page.query_selector(selector)
                if el:
                    box = el.bounding_box()
                    if box and box['height'] > 0:
                        # Add padding
                        pad = 20
                        clip = {
                            'x': max(0, box['x'] - pad),
                            'y': max(0, box['y'] - pad),
                            'width': min(w, box['width'] + pad*2),
                            'height': min(box['height'] + pad*2, 3000)
                        }
                        # Scroll to element first
                        page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")
                        time.sleep(0.3)
                        page.screenshot(
                            path=f'/home/ubuntu/printprosg/audit/{sec_name}_{vp_name}.png',
                            clip=clip
                        )
                        print(f"  {sec_name}: {int(box['width'])}x{int(box['height'])}px")
                    else:
                        print(f"  {sec_name}: HIDDEN or zero height")
                else:
                    print(f"  {sec_name}: NOT FOUND")
            except Exception as e:
                print(f"  {sec_name}: ERROR - {e}")

        page.close()

    browser.close()
    print("\nAll screenshots saved to /home/ubuntu/printprosg/audit/")
