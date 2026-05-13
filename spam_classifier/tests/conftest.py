import pytest
import json
import os
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        # Launch a CLEAN, fast browser in Headed Mode (No profile locks!)
        browser = p.chromium.launch(
            headless=False,
            args=["--window-size=1280,720"]  # Gives you a nice viewing window
        )
        context = browser.new_context()

        # Load the cookies from your saved file
        cookie_file = os.path.join(os.getcwd(), "cookies.json")

        try:
            with open(cookie_file, "r") as f:
                cookies = json.load(f)

                # --- THE BULLETPROOF CLEANER ---
                for cookie in cookies:
                    cookie.pop("sameSite", None)
                    cookie.pop("hostOnly", None)
                    cookie.pop("session", None)
                    cookie.pop("storeId", None)
                    cookie.pop("id", None)
                # -------------------------------

                # Inject the cookies to instantly log in
                context.add_cookies(cookies)
                print("\n[+] Successfully injected Google session cookies.")

        except FileNotFoundError:
            pytest.fail("\nERROR: cookies.json not found! Please export them using Cookie-Editor.")

        yield context
        browser.close()


@pytest.fixture
def gmail_page(browser_context):
    page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
    yield page