import os
from playwright.sync_api import sync_playwright

HEADED = os.getenv("HEADED", "0") == "1"

def run(url: str = "https://example.com"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        print(f"Page title: {title}")
        page.screenshot(path="screenshot.png")
        print("Screenshot saved to screenshot.png")
        browser.close()

if __name__ == "__main__":
    run()
