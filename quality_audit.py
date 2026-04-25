from playwright.sync_api import sync_playwright
import os

os.makedirs("quality_audit", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Use 2x device pixel ratio for high-res screenshots
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2
    )
    page.goto("http://localhost:9090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2500)

    # Dismiss cookie banner
    try:
        page.click("text=Accept All", timeout=2000)
        page.wait_for_timeout(600)
    except:
        pass

    # Full page at 2x resolution
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(500)
    page.screenshot(path="quality_audit/00_full_page_2x.png", full_page=True)
    print("Full page saved")

    # Section by section
    sections = [
        ("window.scrollTo(0,0)", "01_hero.png"),
        ("document.querySelector('#reviews') && document.querySelector('#reviews').scrollIntoView()", "02_reviews.png"),
        ("document.querySelector('#about') && document.querySelector('#about').scrollIntoView()", "03_about.png"),
        ("document.querySelector('#how-it-works') && document.querySelector('#how-it-works').scrollIntoView()", "04_how_it_works.png"),
        ("document.querySelector('#services') && document.querySelector('#services').scrollIntoView()", "05_services.png"),
        ("document.querySelector('#portfolio') && document.querySelector('#portfolio').scrollIntoView()", "06_portfolio.png"),
        ("document.querySelector('#clients') && document.querySelector('#clients').scrollIntoView()", "07_clients.png"),
        ("document.querySelector('#locations') && document.querySelector('#locations').scrollIntoView()", "08_locations.png"),
        ("document.querySelector('#faq') && document.querySelector('#faq').scrollIntoView()", "09_faq.png"),
        ("document.querySelector('#contact') && document.querySelector('#contact').scrollIntoView()", "10_contact.png"),
        ("document.querySelector('footer') && document.querySelector('footer').scrollIntoView()", "11_footer.png"),
    ]

    for js, filename in sections:
        page.evaluate(js)
        page.wait_for_timeout(900)
        page.screenshot(path=f"quality_audit/{filename}", full_page=False)
        print(f"Saved: {filename}")

    browser.close()
    print("All done ✅")
