from playwright.sync_api import Page
import time


class GmailInboxPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_inbox(self):
        print("\nNavigating to Inbox...")
        self.page.goto("https://mail.google.com/mail/u/0/#inbox")
        self.page.wait_for_selector("tr.zA", timeout=30000)

    def extract_and_read_unread_emails(self, limit=50):
        extracted_data = []

        for i in range(limit):
            # Locate the FIRST unread email row (Gmail uses class 'zE' for unread)
            unread_email = self.page.locator("tr.zE").first

            # If no unread emails are found, stop the loop
            if unread_email.count() == 0:
                print("\nNo more unread emails found in the inbox!")
                break

            print(f"Opening unread email {i + 1}...")

            # 1. Click to open the email (This naturally marks it as Read!)
            unread_email.click()

            # 2. Wait for the actual email body to load on the screen
            self.page.wait_for_selector("div.a3s", timeout=15000)

            # 3. Extract the data from the OPEN email view
            # Subject
            subject_loc = self.page.locator("h2.hP").first
            subject = subject_loc.inner_text() if subject_loc.count() > 0 else "No Subject"

            # Sender
            sender_loc = self.page.locator("span.gD").first
            sender = sender_loc.inner_text() + f" <{sender_loc.get_attribute('email')}>" if sender_loc.count() > 0 else "Unknown Sender"

            # Date
            date_loc = self.page.locator("span.g3").first
            date_time = date_loc.get_attribute("title") if date_loc.count() > 0 else "Unknown Date"

            # Full Email Body (Extracts all the text inside the email container)
            body_loc = self.page.locator("div.a3s").first
            full_body = body_loc.inner_text().strip() if body_loc.count() > 0 else "No Text Body"

            # Simple Spam Classification
            classification = "Spam" if "offer" in subject.lower() or "win" in subject.lower() else "Authentic"

            extracted_data.append({
                "sender": sender,
                "date_time": date_time,
                "email_body": full_body,
                "status": "Read",  # It is now read because we opened it
                "classify": classification
            })

            # 4. Go back to the Inbox
            back_button = self.page.locator("div[aria-label='Back to Inbox']").first
            if back_button.count() > 0:
                back_button.click()
            else:
                self.page.goto("https://mail.google.com/mail/u/0/#inbox")

            # Wait for the inbox list to reappear before looping again
            self.page.wait_for_selector("tr.zA", timeout=15000)

            # Pause for 1 second to let Gmail's UI settle
            time.sleep(1)

        return extracted_data