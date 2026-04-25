from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(2000)

    def get_styles(selector, props):
        el = page.query_selector(selector)
        if not el:
            return f"  {selector}: NOT FOUND"
        box = el.bounding_box()
        result = [f"  {selector}: {box['height']:.0f}px tall" if box else f"  {selector}: no box"]
        for prop in props:
            val = page.evaluate(f'el => window.getComputedStyle(el).{prop}', el)
            result.append(f"    {prop}: {val}")
        return "\n".join(result)

    print("=== HERO ===")
    print(get_styles('#hero', ['paddingTop', 'paddingBottom', 'minHeight', 'height']))
    print(get_styles('.hero-inner', ['paddingTop', 'paddingBottom', 'gap', 'flexDirection']))
    print(get_styles('.hero-content', ['paddingTop', 'paddingBottom', 'marginBottom']))
    print(get_styles('.hero-sub', ['display', 'fontSize', 'marginBottom']))
    print(get_styles('.hero-ctas', ['flexDirection', 'gap', 'marginBottom']))
    print(get_styles('.hero-ctas a:first-child', ['width', 'height', 'borderRadius', 'display']))
    print(get_styles('.hero-product-showcase', ['gridTemplateColumns', 'gap', 'marginTop']))
    print(get_styles('.hero-product-card:first-child', ['height', 'padding']))

    print("\n=== FOOTER ===")
    print(get_styles('footer', ['paddingTop', 'paddingBottom', 'height']))
    print(get_styles('.footer-grid', ['display', 'gridTemplateColumns', 'gap']))
    print(get_styles('.footer-col:nth-child(3)', ['display']))
    print(get_styles('.footer-col:nth-child(4)', ['display']))

    print("\n=== ABOUT ===")
    print(get_styles('#about', ['paddingTop', 'paddingBottom']))
    print(get_styles('.about-content > p', ['display', 'fontSize']))
    print(get_styles('.about-stats', ['gridTemplateColumns', 'gap']))

    print("\n=== SERVICES ===")
    print(get_styles('#services', ['paddingTop', 'paddingBottom']))
    print(get_styles('.services-grid', ['gridTemplateColumns', 'gap']))
    print(get_styles('.service-card:first-child', ['height', 'borderRadius']))
    print(get_styles('.service-img', ['height']))

    browser.close()
