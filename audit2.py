from playwright.sync_api import sync_playwright
import time, os

os.makedirs('/home/ubuntu/printprosg/audit2', exist_ok=True)

SECTIONS = [
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
    ('mobile', 390, 844),
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for vp_name, w, h in VIEWPORTS:
        print(f"\n=== {vp_name.upper()} ({w}x{h}) ===")
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.goto('http://localhost:8090/', wait_until='networkidle')
        time.sleep(2)

        # Close announcement bar
        try:
            page.click('#close-announcement', timeout=2000)
            time.sleep(0.3)
        except:
            pass

        # Full page screenshot
        page.screenshot(
            path=f'/home/ubuntu/printprosg/audit2/full_{vp_name}.png',
            full_page=True
        )

        # Per-section: scroll to element, wait, screenshot the element bounding box
        for sec_name, selector in SECTIONS:
            try:
                el = page.query_selector(selector)
                if not el:
                    print(f"  {sec_name}: NOT FOUND")
                    continue

                # Scroll into view
                page.evaluate(f"""
                    var el = document.querySelector('{selector}');
                    if (el) el.scrollIntoView({{block: 'start'}});
                """)
                time.sleep(0.5)

                box = el.bounding_box()
                if not box or box['height'] == 0:
                    print(f"  {sec_name}: zero height")
                    continue

                # For tall sections, take multiple screenshots
                section_h = int(box['height'])
                section_y = int(box['y'])
                section_x = max(0, int(box['x']))
                section_w = min(w, int(box['width']))

                if section_h <= h * 1.5:
                    # Single screenshot
                    page.evaluate(f"""
                        var el = document.querySelector('{selector}');
                        if (el) el.scrollIntoView({{block: 'start'}});
                    """)
                    time.sleep(0.4)
                    # Get updated box after scroll
                    box2 = el.bounding_box()
                    if box2:
                        clip = {
                            'x': max(0, box2['x']),
                            'y': max(0, box2['y']),
                            'width': min(w, box2['width']),
                            'height': min(box2['height'], h * 2)
                        }
                        if clip['width'] > 0 and clip['height'] > 0:
                            page.screenshot(
                                path=f'/home/ubuntu/printprosg/audit2/{sec_name}_{vp_name}.png',
                                clip=clip
                            )
                            print(f"  {sec_name}: {section_w}x{section_h}px ✓")
                        else:
                            print(f"  {sec_name}: invalid clip {clip}")
                else:
                    # Tall section: use full_page clip approach
                    page.screenshot(
                        path=f'/home/ubuntu/printprosg/audit2/{sec_name}_{vp_name}.png',
                        full_page=True,
                        clip={'x': 0, 'y': section_y, 'width': w, 'height': min(section_h, 3000)}
                    )
                    print(f"  {sec_name}: {section_w}x{section_h}px (tall) ✓")

            except Exception as e:
                print(f"  {sec_name}: ERROR - {str(e)[:80]}")

        page.close()

    browser.close()
    print("\nDone.")
