from playwright.sync_api import sync_playwright

tabs_to_test = [
    ('most-popular', 'Most Popular'),
    ('name-cards', 'Name Cards'),
    ('flyers', 'Flyers & Leaflets'),
    ('stickers', 'Stickers'),
    ('booklets', 'Booklets'),
    ('stationery', 'Stationery & Cards'),
    ('marketing', 'Marketing & Advertising'),
    ('signages', 'Signages'),
    ('promo', 'Promo & Giveaways'),
    ('displays', 'Displays & Banners'),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(1000)

    for filter_val, label in tabs_to_test:
        tab = page.locator(f'.nav-cat[data-filter="{filter_val}"]')
        tab.click()
        page.wait_for_timeout(500)

        # Count cards that are visible (not hidden by card-hidden or hidden-default)
        visible_count = page.evaluate("""
            (function() {
                var cards = document.querySelectorAll('#services-grid .service-card');
                var count = 0;
                cards.forEach(function(c) {
                    var hidden = c.classList.contains('card-hidden') || c.classList.contains('hidden-default');
                    if (!hidden) { count++; }
                });
                return count;
            })()
        """)
        print(f'{label}: {visible_count} cards')

    browser.close()
    print("Done.")
