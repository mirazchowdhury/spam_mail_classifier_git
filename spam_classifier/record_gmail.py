from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import os

# 1. COMPLETELY CLOSE all other Chrome windows before running this!
# 2. Use a unique folder name to avoid profile locks
USER_DATA_DIR = os.path.join(os.getcwd(), "gmail_recorder_profile")

with sync_playwright() as p:
    # Launch with a persistent context (essential for Gmail)
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",  # Use real Chrome
        args=["--disable-blink-features=AutomationControlled"]
    )

    # Persistent context automatically opens one page
    page = context.pages[0]

    # Apply stealth to hide automation markers
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    print("Navigating to Gmail...")
    # Navigate FIRST, then pause to use codegen/inspector
    page.goto("https://accounts.google.com", wait_until="networkidle")

    print("Opening Inspector. Use the Record button to get your objects.")
    page.pause()

