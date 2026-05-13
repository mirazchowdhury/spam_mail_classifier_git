from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth  # Use the new Stealth class

with sync_playwright() as p:
    # Use 'chrome' channel and a persistent context to build trust with Google
    context = p.chromium.launch_persistent_context(
        user_data_dir="google_profile",
        headless=False,
        channel="chrome"
    )

    # Get the automatically created first page
    page = context.pages[0]

    # Apply stealth using the new class-based method
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    page.goto("https://gmail.com")

    print("Log in manually. The 'not secure' error should now be gone.")
    page.pause()
