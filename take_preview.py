from playwright.sync_api import sync_playwright
import os

os.makedirs("preview_final", exist_ok=True)

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

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://localhost:9090/index.html", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Dismiss cookie banner if present
    try:
        page.click("text=Accept All", timeout=2000)
        page.wait_for_timeout(500)
    except:
        pass

    for js, filename in sections:
        page.evaluate(js)
        page.wait_for_timeout(800)
        page.screenshot(path=f"preview_final/{filename}", full_page=False)
        print(f"Saved: {filename}")

    # Full page
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(500)
    page.screenshot(path="preview_final/00_full_page.png", full_page=True)
    print("Saved: 00_full_page.png")

    browser.close()
    print("All screenshots done ✅")
