from playwright.sync_api import sync_playwright
import os

os.makedirs('/home/ubuntu/printprosg/v52_verify', exist_ok=True)

def safe_section_shot(page, selector, path, extra_height=0):
    try:
        el = page.locator(selector)
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        bb = el.bounding_box()
        if bb:
            vw = page.viewport_size['width']
            vh = page.viewport_size['height']
            h = min(int(bb['height']) + extra_height, 900)
            page.screenshot(path=path, clip={
                'x': 0,
                'y': max(0, bb['y']),
                'width': vw,
                'height': h
            })
    except Exception as e:
        print(f'Skipped {path}: {e}')

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ── DESKTOP 1440px ──────────────────────────────────────────────
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    # Navbar
    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/01_navbar.png',
                    clip={'x': 0, 'y': 0, 'width': 1440, 'height': 160})

    # Hero
    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/03_hero.png',
                    clip={'x': 0, 'y': 160, 'width': 1440, 'height': 600})

    # Reviews
    safe_section_shot(page, '#reviews', '/home/ubuntu/printprosg/v52_verify/04_reviews.png', 100)

    # About
    safe_section_shot(page, '#about', '/home/ubuntu/printprosg/v52_verify/05_about.png', 100)

    # Services
    safe_section_shot(page, '#services', '/home/ubuntu/printprosg/v52_verify/06_services.png', 200)

    # Locations
    safe_section_shot(page, '#locations', '/home/ubuntu/printprosg/v52_verify/08_locations.png', 100)

    # FAQ
    safe_section_shot(page, '#faq', '/home/ubuntu/printprosg/v52_verify/09_faq.png', 100)

    # Contact
    safe_section_shot(page, '#contact', '/home/ubuntu/printprosg/v52_verify/10_contact.png', 100)

    # Footer — scroll to bottom
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_timeout(600)
    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/11_footer.png',
                    clip={'x': 0, 'y': max(0, page.evaluate('document.body.scrollHeight - 500')), 'width': 1440, 'height': 500})

    # Cookie banner
    try:
        cookie = page.locator('#cookie-banner')
        if cookie.is_visible():
            page.screenshot(path='/home/ubuntu/printprosg/v52_verify/12_cookie.png',
                            clip={'x': 0, 'y': max(0, page.evaluate('window.innerHeight') - 80), 'width': 1440, 'height': 80})
    except Exception as e:
        print(f'Cookie skipped: {e}')

    # ── MOBILE 390px ────────────────────────────────────────────────
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/13_mobile_navbar.png',
                    clip={'x': 0, 'y': 0, 'width': 390, 'height': 130})

    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/14_mobile_hero.png',
                    clip={'x': 0, 'y': 130, 'width': 390, 'height': 600})

    safe_section_shot(page, '#services', '/home/ubuntu/printprosg/v52_verify/15_mobile_services.png', 200)

    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_timeout(600)
    page.screenshot(path='/home/ubuntu/printprosg/v52_verify/16_mobile_footer.png',
                    clip={'x': 0, 'y': max(0, page.evaluate('document.body.scrollHeight - 500')), 'width': 390, 'height': 500})

    browser.close()

print("All v52 verification screenshots captured.")
