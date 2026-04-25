#!/usr/bin/env python3
"""Verify mobile fixes: WhatsApp bubble hidden, portfolio filters horizontal scroll."""
from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/home/ubuntu/printprosg/final_verify"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    # iPhone 14 viewport
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2
    )
    page.goto("http://localhost:9090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Check WhatsApp bubble
    wa_result = page.evaluate("""() => {
        const el = document.querySelector('.whatsapp-float');
        if (!el) return 'NOT FOUND';
        return {
            inlineStyle: el.getAttribute('style'),
            computedDisplay: window.getComputedStyle(el).display,
            visible: el.offsetParent !== null
        };
    }""")
    print("WhatsApp float:", wa_result)

    # Check portfolio filters
    pf_result = page.evaluate("""() => {
        const el = document.querySelector('.portfolio-filters');
        if (!el) return 'NOT FOUND';
        const style = el.getAttribute('style');
        const computed = window.getComputedStyle(el);
        return {
            inlineStyle: style,
            computedFlexWrap: computed.flexWrap,
            computedOverflowX: computed.overflowX
        };
    }""")
    print("Portfolio filters:", pf_result)

    # Screenshot 1: Full page bottom area (to check WhatsApp bubble)
    page.screenshot(path=f"{OUTPUT_DIR}/01_full_bottom.png", full_page=False)
    print("Screenshot 1: viewport (bottom area check)")

    # Scroll to portfolio section
    page.evaluate("document.querySelector('.portfolio-filters').scrollIntoView({behavior: 'instant', block: 'center'})")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUTPUT_DIR}/02_portfolio_filters.png", full_page=False)
    print("Screenshot 2: portfolio filters section")

    # Scroll to hero
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUTPUT_DIR}/03_hero.png", full_page=False)
    print("Screenshot 3: hero section")

    # Full page screenshot
    page.screenshot(path=f"{OUTPUT_DIR}/04_full_page.png", full_page=True)
    print("Screenshot 4: full page")

    browser.close()

print(f"\nAll screenshots saved to {OUTPUT_DIR}")
