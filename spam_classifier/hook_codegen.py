from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 1. Connect to the browser you opened in Step 1
    # This must match the port 9222 you used in the terminal
    browser = p.chromium.connect_over_cdp("http://localhost:9222")

    # 2. Access the existing context (your logged-in session)
    context = browser.contexts[0]

    # 3. Get the Gmail page that is already open
    # If you have multiple tabs, this picks the first one
    page = context.pages[0]

    print("Successfully connected to your Chrome window!")
    print("Opening the Playwright Inspector now...")

    # 4. This command starts the 'codegen' interface (Inspector)
    # on your existing, live Gmail page.
    page.pause()
