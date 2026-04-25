from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1500)

    # Measure hero-content children
    children = page.evaluate('''() => {
        const content = document.querySelector('.hero-content');
        if (!content) return [];
        return Array.from(content.children).map(el => ({
            tag: el.tagName,
            class: el.className,
            height: el.getBoundingClientRect().height,
            display: window.getComputedStyle(el).display,
            marginBottom: window.getComputedStyle(el).marginBottom
        }));
    }''')
    
    print("=== HERO-CONTENT CHILDREN ===")
    total = 0
    for c in children:
        print(f"  <{c['tag']}> .{c['class']}: h={c['height']:.0f}px, display={c['display']}, mb={c['marginBottom']}")
        total += c['height']
    print(f"  Total content height: {total:.0f}px")
    
    # Hero-content itself
    hc = page.query_selector('.hero-content')
    if hc:
        box = hc.bounding_box()
        print(f"\nHero-content box: {box['height']:.0f}px")
    
    # Hero trust row
    trust = page.query_selector('.hero-trust-row')
    if trust:
        box = trust.bounding_box()
        print(f"Trust row: {box['height']:.0f}px")
    
    # Hero ctas
    ctas = page.query_selector('.hero-ctas')
    if ctas:
        box = ctas.bounding_box()
        print(f"Hero CTAs: {box['height']:.0f}px")
    
    # Hero product showcase
    showcase = page.query_selector('.hero-product-showcase')
    if showcase:
        box = showcase.bounding_box()
        print(f"Product showcase: {box['height']:.0f}px")
    
    # Hero section padding
    hero = page.query_selector('#hero')
    if hero:
        pt = page.evaluate('el => window.getComputedStyle(el).paddingTop', hero)
        pb = page.evaluate('el => window.getComputedStyle(el).paddingBottom', pb := hero)
        print(f"\nHero padding: top={pt}, bottom={pb}")
    
    browser.close()
