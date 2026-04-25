#!/usr/bin/env python3
"""Take final full-page mobile screenshot at 390px viewport for visual audit."""

from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/home/ubuntu/printprosg/v53_final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///home/ubuntu/printprosg/index.html', wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    # Full page screenshot
    page.screenshot(path=f"{OUTPUT_DIR}/full_page_mobile.png", full_page=True)
    print(f"Full page screenshot saved to {OUTPUT_DIR}/full_page_mobile.png")
    
    # Take section screenshots for visual audit
    sections = [
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
    
    for name, selector in sections:
        try:
            el = page.query_selector(selector)
            if el:
                el.screenshot(path=f"{OUTPUT_DIR}/{name}.png")
                box = el.bounding_box()
                print(f"  {name}: {box['height']:.0f}px")
        except Exception as e:
            print(f"  {name}: ERROR - {e}")
    
    browser.close()
    print("Done!")
