import imaplib
import email
from email.header import decode_header
import json
import os
import re
import html
from bs4 import BeautifulSoup


# --- YOUR CREDENTIALS ---
EMAIL_ACCOUNT = "mirazchowdhury03@gmail.com"  # Your Gmail
APP_PASSWORD = "bmbd yibi cref dldr"  # Put your 16-letter App Password here


# ------------------------

def safe_decode_header(header_value):
    """Safely decodes email headers, ignoring fake or corrupted encodings."""
    if not header_value:
        return ""

    decoded_parts = decode_header(header_value)
    result = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                result += part.decode(encoding or "utf-8", errors="ignore")
            except LookupError:
                result += part.decode("utf-8", errors="ignore")
        else:
            result += str(part)

    return result





def clean_text(raw_html):
    """Dynamically extracts text and URLs from ANY HTML newsletter."""

    raw_html = html.unescape(raw_html)
    soup = BeautifulSoup(raw_html, 'html.parser')

    # 1. Kill all hidden scripts and styles just in case
    for element in soup(["script", "style"]):
        element.decompose()

    # 2. DYNAMIC LINK EXTRACTION: Find every single link in the email
    for a_tag in soup.find_all('a'):
        link_text = a_tag.get_text(strip=True)
        href = a_tag.get('href')

        # If it's a valid link with text, rewrite it so the URL doesn't get lost!
        if link_text and href and href.startswith('http'):
            # Formats it dynamically like: "Click Here (https://...)"
            new_text = f"{link_text} ({href})"
            a_tag.replace_with(new_text)

    # 3. Extract the text with double-newlines for paragraphs
    text = soup.get_text(separator='\n\n', strip=True)

    # 4. Clean up any massive gaps of empty space
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def get_email_body(msg):
    """Extracts the body and falls back to HTML if plain text is missing."""
    body = ""
    html_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            if content_type == "text/plain":
                try:
                    body += part.get_payload(decode=True).decode(errors="ignore")
                except Exception:
                    pass
            elif content_type == "text/html":
                try:
                    html_body += part.get_payload(decode=True).decode(errors="ignore")
                except Exception:
                    pass
    else:
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True).decode(errors="ignore")
            if content_type == "text/html":
                html_body = payload
            else:
                body = payload
        except Exception:
            pass

    final_raw_text = body if body.strip() else html_body
    return clean_text(final_raw_text)


# --- ADDED LIMIT BACK HERE ---
def get_emails(limit=5):
    print("Connecting to Gmail...")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)

    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    # --- GRAB ONLY THE LATEST 30 ---
    latest_email_ids = email_ids[-limit:]
    latest_email_ids.reverse()

    extracted_data = []
    total_emails = len(latest_email_ids)

    if total_emails == 0:
        print("You have no unread emails!")
        return []

    print(f"Fetching, cleaning, and marking {total_emails} UNREAD emails as Read...")

    for index, e_id in enumerate(latest_email_ids):
        try:
            # (RFC822) forces Gmail to mark it as READ
            res, msg_data = mail.fetch(e_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    status = "Read"

                    sender = safe_decode_header(msg.get("From", ""))
                    subject = safe_decode_header(msg.get("Subject", ""))
                    date_time = msg.get("Date", "")

                    full_body = get_email_body(msg)
                    if not full_body:
                        full_body = f"[No Text Body] Subject: {subject}"

                    classification = "Spam" if "offer" in subject.lower() or "win" in subject.lower() else "Authentic"

                    extracted_data.append({
                        "sender": sender,
                        "date_time": date_time,
                        "subject": subject,
                        "email_body": full_body
                    })
        except Exception as e:
            print(f"Skipped an email due to error: {e}")
            continue

    mail.logout()
    return extracted_data


if __name__ == "__main__":
    # Calls the function with the limit applied
    emails = get_emails(limit=5)

    data_path = os.path.join(os.getcwd(), "data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=4)

    print(f"\n[SUCCESS] Extracted and cleaned {len(emails)} emails. They are now marked as Read!")