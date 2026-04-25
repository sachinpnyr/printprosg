from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8090/', wait_until='networkidle')
    time.sleep(2)
    
    # Check contact section
    result = page.evaluate("""() => {
        const info = document.querySelector('#contact .contact-info');
        const h2 = document.querySelector('#contact .contact-info h2');
        const details = document.querySelector('#contact .contact-details');
        const payment = document.querySelector('#contact .payment-methods');
        const p = document.querySelector('#contact .contact-info > p');
        const eyebrow = document.querySelector('#contact .contact-info .eyebrow');
        return {
            info_h: info ? info.offsetHeight : 0,
            info_display: info ? window.getComputedStyle(info).display : 'N/A',
            h2_h: h2 ? h2.offsetHeight : 0,
            h2_display: h2 ? window.getComputedStyle(h2).display : 'N/A',
            details_display: details ? window.getComputedStyle(details).display : 'N/A',
            payment_display: payment ? window.getComputedStyle(payment).display : 'N/A',
            p_display: p ? window.getComputedStyle(p).display : 'N/A',
            eyebrow_display: eyebrow ? window.getComputedStyle(eyebrow).display : 'N/A',
        };
    }""")
    print("Contact info:", result)
    
    # Total heights
    sections = page.evaluate("""() => {
        const ids = ['hero','reviews','about','how-it-works','services','portfolio','clients','locations','faq','contact'];
        return ids.map(id => {
            const el = document.getElementById(id);
            if (!el) return {id: id, h: 0};
            return {id: id, h: Math.round(el.offsetHeight)};
        });
    }""")
    total = sum(s['h'] for s in sections)
    for s in sections:
        print(f"  #{s['id']:20s}: {s['h']}px")
    print(f"\nTotal sections: {total}px")
    print(f"Full page: {page.evaluate('document.body.scrollHeight')}px")
    
    # Screenshot contact
    contact_el = page.query_selector('#contact')
    if contact_el:
        contact_el.screenshot(path='/home/ubuntu/printprosg/screenshots_v51/contact_fixed_390.png')
        print("Contact screenshot saved")
    
    browser.close()
