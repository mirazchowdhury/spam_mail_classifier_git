from seleniumbase import Driver
import time

# This launches a browser that is invisible to Google's bot detection
driver = Driver(uc=True, headed=True)

try:
    driver.get("https://accounts.google.com")
    print("Log in manually now. The 'not secure' error will not appear.")

    # Keep the window open for 5 minutes so you can finish logging in
    time.sleep(300)
finally:
    driver.quit()
