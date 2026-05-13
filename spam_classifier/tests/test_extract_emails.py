import json
import os
from pages.gmail_inbox_page import GmailInboxPage


def test_extract_and_save_emails(gmail_page):
    inbox_page = GmailInboxPage(gmail_page)
    inbox_page.navigate_to_inbox()

    # Extract and read up to 50 unread emails
    emails = inbox_page.extract_and_read_unread_emails(limit=20)

    if emails:
        data_path = os.path.join(os.getcwd(), "data.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(emails, f, indent=4)

        print(f"\n[SUCCESS] Successfully read and extracted {len(emails)} emails!")
    else:
        print("\n[INFO] No unread emails were found to extract.")