from playwright.sync_api import sync_playwright
import os, json

os.makedirs('/home/ubuntu/printprosg/apple_audit', exist_ok=True)

def measure(page, selector):
    el = page.query_selector(selector)
    if not el:
        return None
    box = el.bounding_box()
    if not box:
        return None
    return {
        'height': round(box['height'], 1),
        'width': round(box['width'], 1),
        'x': round(box['x'], 1),
        'y': round(box['y'], 1),
        'font_size': page.evaluate('el => window.getComputedStyle(el).fontSize', el),
        'font_weight': page.evaluate('el => window.getComputedStyle(el).fontWeight', el),
        'line_height': page.evaluate('el => window.getComputedStyle(el).lineHeight', el),
        'letter_spacing': page.evaluate('el => window.getComputedStyle(el).letterSpacing', el),
        'padding': page.evaluate('el => window.getComputedStyle(el).padding', el),
        'border_radius': page.evaluate('el => window.getComputedStyle(el).borderRadius', el),
        'color': page.evaluate('el => window.getComputedStyle(el).color', el),
        'background': page.evaluate('el => window.getComputedStyle(el).backgroundColor', el),
    }

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('https://www.apple.com', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Dismiss country selector
    try:
        page.click('#ac-ls-close', timeout=3000)
        page.wait_for_timeout(800)
    except:
        pass

    # Screenshots
    page.screenshot(path='/home/ubuntu/printprosg/apple_audit/apple_mobile_full.png', full_page=True)
    page.screenshot(path='/home/ubuntu/printprosg/apple_audit/apple_navbar.png',
                   clip={'x': 0, 'y': 0, 'width': 390, 'height': 90})
    page.screenshot(path='/home/ubuntu/printprosg/apple_audit/apple_hero.png',
                   clip={'x': 0, 'y': 0, 'width': 390, 'height': 700})

    results = {}

    # Navbar
    nav = page.query_selector('#globalnav')
    if nav:
        box = nav.bounding_box()
        results['navbar'] = {
            'height': round(box['height'], 1),
            'padding_top': page.evaluate('el => window.getComputedStyle(el).paddingTop', nav),
            'padding_bottom': page.evaluate('el => window.getComputedStyle(el).paddingBottom', nav),
            'background': page.evaluate('el => window.getComputedStyle(el).backgroundColor', nav),
        }

    # All headings on page
    headings = page.query_selector_all('h1, h2, h3')
    for i, h in enumerate(headings[:5]):
        box = h.bounding_box()
        if box:
            results[f'heading_{i}'] = {
                'tag': page.evaluate('el => el.tagName', h),
                'text': page.evaluate('el => el.textContent.trim().substring(0, 50)', h),
                'font_size': page.evaluate('el => window.getComputedStyle(el).fontSize', h),
                'font_weight': page.evaluate('el => window.getComputedStyle(el).fontWeight', h),
                'line_height': page.evaluate('el => window.getComputedStyle(el).lineHeight', h),
                'letter_spacing': page.evaluate('el => window.getComputedStyle(el).letterSpacing', h),
                'height': round(box['height'], 1),
            }

    # Buttons
    buttons = page.query_selector_all('a.button, .button-primary, .button-secondary')
    for i, btn in enumerate(buttons[:4]):
        box = btn.bounding_box()
        if box:
            results[f'button_{i}'] = {
                'text': page.evaluate('el => el.textContent.trim()', btn),
                'height': round(box['height'], 1),
                'width': round(box['width'], 1),
                'font_size': page.evaluate('el => window.getComputedStyle(el).fontSize', btn),
                'font_weight': page.evaluate('el => window.getComputedStyle(el).fontWeight', btn),
                'border_radius': page.evaluate('el => window.getComputedStyle(el).borderRadius', btn),
                'padding': page.evaluate('el => window.getComputedStyle(el).padding', btn),
                'background': page.evaluate('el => window.getComputedStyle(el).backgroundColor', btn),
            }

    # Body
    body = page.query_selector('body')
    results['body'] = {
        'font_family': page.evaluate('el => window.getComputedStyle(el).fontFamily', body),
        'font_size': page.evaluate('el => window.getComputedStyle(el).fontSize', body),
        'color': page.evaluate('el => window.getComputedStyle(el).color', body),
    }

    # Section padding
    sections = page.query_selector_all('section')
    if sections:
        s = sections[0]
        results['first_section'] = {
            'padding_top': page.evaluate('el => window.getComputedStyle(el).paddingTop', s),
            'padding_bottom': page.evaluate('el => window.getComputedStyle(el).paddingBottom', s),
            'padding_left': page.evaluate('el => window.getComputedStyle(el).paddingLeft', s),
            'padding_right': page.evaluate('el => window.getComputedStyle(el).paddingRight', s),
        }

    print("=== APPLE.COM MOBILE MEASUREMENTS (390px) ===")
    print(json.dumps(results, indent=2))

    with open('/home/ubuntu/printprosg/apple_audit/measurements.json', 'w') as f:
        json.dump(results, f, indent=2)

    browser.close()
