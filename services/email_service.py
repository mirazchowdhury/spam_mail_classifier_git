# services/email_service.py
import imaplib
import email
from email.header import decode_header
import html2text
from bs4 import BeautifulSoup
import re
from config import EMAIL_ACCOUNT, APP_PASSWORD


def safe_decode_header(header_value):
    if not header_value: return ""
    decoded_parts = decode_header(header_value)
    result = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                result += part.decode(encoding or "utf-8", errors="ignore")
            except:
                result += part.decode("utf-8", errors="ignore")
        else:
            result += str(part)
    return result


def extract_links(html_content):
    if not html_content: return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        if len(text) > 2 and "http" in href and "unsubscribe" not in href.lower():
            links.append(f"- {text}: {href}")
    return "\n".join(list(set(links))[:5])


def get_email_content(msg):
    text_body = ""
    html_body = ""
    image_parts = []
    doc_parts = [] # NEW: Document parts list

    for part in msg.walk():
        content_type = part.get_content_type()
        filename = part.get_filename()

        if content_type == "text/plain" and not filename:
            try: text_body += part.get_payload(decode=True).decode(errors="ignore")
            except: pass
        elif content_type == "text/html" and not filename:
            try: html_body += part.get_payload(decode=True).decode(errors="ignore")
            except: pass
        elif "image" in content_type:
            image_parts.append(part)
        # NEW: PDF ebong Word file detect kora
        elif filename and filename.lower().endswith((".pdf", ".docx", ".doc")):
            doc_parts.append(part)

    # --- NEW: HTML Deep Cleaning Logic ---
    clean_html_text = ""
    if html_body:
        soup = BeautifulSoup(html_body, 'html.parser')
        # Remove junk elements that confuse the AI
        for element in soup(["script", "style", "meta", "noscript", "header", "footer", "nav"]):
            element.decompose()

        # Get readable text and remove massive empty spaces
        raw_text = soup.get_text(separator=' ', strip=True)
        clean_html_text = re.sub(r'\s+', ' ', raw_text)  # Shrinks all spaces to a single space

    # Decide which text to use
    final_text = text_body if len(text_body) > len(clean_html_text) else clean_html_text

    # Still extract links from the raw HTML
    extracted_links = extract_links(html_body)

    return final_text, html_body, image_parts, doc_parts


def fetch_latest_emails(limit=20):
    print("Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    latest_email_ids = messages[0].split()[-limit:]
    latest_email_ids.reverse()

    emails_data = []
    print(f"Fetching {len(latest_email_ids)} emails...")

    for e_id in latest_email_ids:
        try:
            res, msg_data = mail.fetch(e_id, "(BODY.PEEK[] FLAGS)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    sender = safe_decode_header(msg.get("From", ""))
                    subject = safe_decode_header(msg.get("Subject", ""))
                    date_time = msg.get("Date", "")

                    emails_data.append({
                        'sender': sender,
                        'subject': subject,
                        'date': date_time,
                        'raw_msg': msg
                    })
        except Exception as e:
            print(f"Error fetching an email: {e}")

    mail.logout()
    return emails_data