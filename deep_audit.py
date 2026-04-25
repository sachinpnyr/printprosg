from playwright.sync_api import sync_playwright
import time, os

os.makedirs('/home/ubuntu/printprosg/deep_audit', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)

    # Close cookie/announcement
    try:
        page.click('#close-announcement', timeout=2000)
        time.sleep(0.3)
    except:
        pass

    def snap(name, selector=None, x=None, y=None, w=None, h=None, scroll_to=None):
        try:
            if scroll_to:
                page.evaluate(f"document.querySelector('{scroll_to}').scrollIntoView({{block:'center'}})")
                time.sleep(0.5)
            if selector:
                el = page.query_selector(selector)
                if not el:
                    print(f"  {name}: NOT FOUND")
                    return
                box = el.bounding_box()
                if not box:
                    print(f"  {name}: no bounding box")
                    return
                pad = 8
                clip = {
                    'x': max(0, box['x'] - pad),
                    'y': max(0, box['y'] - pad),
                    'width': min(1440, box['width'] + pad*2),
                    'height': min(box['height'] + pad*2, 2000)
                }
            else:
                clip = {'x': x, 'y': y, 'width': w, 'height': h}
            page.screenshot(path=f'/home/ubuntu/printprosg/deep_audit/{name}.png', clip=clip)
            print(f"  {name}: saved")
        except Exception as e:
            print(f"  {name}: ERROR {str(e)[:60]}")

    print("=== NAVBAR ELEMENTS ===")
    snap('nav_logo', '.nav-logo')
    snap('nav_search', '.nav-search')
    snap('nav_right_buttons', '.nav-right')
    snap('nav_category_tabs', '.nav-cat-container')
    snap('nav_trust_bar', '.nav-trust-bar')
    snap('nav_full', '#navbar')

    print("=== HERO ELEMENTS ===")
    page.evaluate("document.querySelector('#hero').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('hero_full', '#hero')
    snap('hero_content', '.hero-content')
    snap('hero_headline', '.hero-headline')
    snap('hero_ctas', '.hero-ctas')
    snap('hero_trust_row', '.hero-trust-row')
    snap('hero_product_cards', '.hero-product-showcase')

    print("=== REVIEWS ELEMENTS ===")
    page.evaluate("document.querySelector('#reviews').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('reviews_header', '#reviews .section-header')
    snap('reviews_card_1', '#reviews .review-card:first-child')
    snap('reviews_carousel', '.reviews-carousel-wrap')

    print("=== ABOUT ELEMENTS ===")
    page.evaluate("document.querySelector('#about').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('about_full', '#about')
    snap('about_stats', '.about-stats')
    snap('about_features', '.about-features')
    snap('about_cta', '#about .btn')

    print("=== HOW IT WORKS ===")
    page.evaluate("document.querySelector('#how-it-works').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('hiw_full', '#how-it-works')
    snap('hiw_step_1', '.hiw-step:first-child')

    print("=== SERVICES ===")
    page.evaluate("document.querySelector('#services').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('services_header', '#services .section-header')
    snap('services_card_1', '.service-card:first-child')
    snap('services_grid_top', '#services-grid')

    print("=== PORTFOLIO ===")
    page.evaluate("document.querySelector('#portfolio').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('portfolio_header', '#portfolio .section-header')
    snap('portfolio_filters', '.portfolio-filters')
    snap('portfolio_item_1', '.portfolio-item:first-child')

    print("=== LOCATIONS ===")
    page.evaluate("document.querySelector('#locations').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('locations_full', '#locations')
    snap('location_card_sg', '.location-card:first-child')

    print("=== FAQ ===")
    page.evaluate("document.querySelector('#faq').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('faq_full', '#faq')
    snap('faq_item_1', '.faq-item:first-child')

    print("=== CONTACT ===")
    page.evaluate("document.querySelector('#contact').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('contact_full', '#contact')
    snap('contact_form', '.contact-form-wrap')
    snap('contact_info', '.contact-info')

    print("=== FOOTER ===")
    page.evaluate("document.querySelector('footer').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('footer_full', 'footer')
    snap('footer_logo', '.footer-brand')
    snap('footer_links', '.footer-links')
    snap('footer_bottom', '.footer-bottom')

    # Now mobile
    page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    try:
        page.click('#close-announcement', timeout=2000)
        time.sleep(0.3)
    except:
        pass

    print("=== MOBILE ELEMENTS ===")
    snap('mobile_navbar', '#navbar')
    snap('mobile_hero', '#hero')

    page.evaluate("document.querySelector('#services').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('mobile_service_card', '.service-card:first-child')

    page.evaluate("document.querySelector('footer').scrollIntoView({block:'start'})")
    time.sleep(0.5)
    snap('mobile_footer', 'footer')
    snap('mobile_footer_logo', '.footer-brand')

    browser.close()
    print("\nDeep audit screenshots complete.")
