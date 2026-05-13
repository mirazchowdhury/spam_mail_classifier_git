# main.py
from services.email_service import fetch_latest_emails, get_email_content
from services.ocr_service import process_all_images
from services.sheets_service import setup_google_sheets, append_batch_to_sheet
from services.ai_service import analyze_email_with_ollama
from services.document_service import process_all_attachments


def run_triage_pipeline(limit=120):
    sheet, existing_signatures = setup_google_sheets()
    emails = fetch_latest_emails(limit)

    new_rows_to_add = []

    for msg_data in emails:
        # 1. Extract basic info
        sender = msg_data['sender']
        subject = msg_data['subject']
        date_time = msg_data['date']

        signature = f"{subject} | {date_time}"
        if signature in existing_signatures:
            continue

        # ... loop-er bhetore ...
        body_text, html_content, image_list, doc_list = get_email_content(msg_data['raw_msg'])

        # 1. OCR text extraction
        ocr_result = process_all_images(image_list)

        # 2. Document text extraction (PDF/DOC)
        doc_result = process_all_attachments(doc_list)

        # 3. Create Super-Context for Llama
        full_context = f"""
        TEXT CONTENT: {body_text}
        IMAGE CONTENT: {ocr_result}
        ATTACHED DOCUMENTS: {doc_result}
        """.strip()

        # 4. Analyze with Ollama
        actionable, summary = analyze_email_with_ollama(subject, full_context)

        # 5. Prepare row for Google Sheets (Truncating full_context to save Sheet limits)
        new_rows_to_add.append([sender, date_time, subject, full_context[:1500], summary, actionable])
        existing_signatures.add(signature)

    # 6. Save to Sheets in one batch
    if new_rows_to_add:
        append_batch_to_sheet(sheet, new_rows_to_add)
        print(f"\n[SUCCESS] Uploaded {len(new_rows_to_add)} emails.")
    else:
        print("\n[SUCCESS] No new emails.")


if __name__ == "__main__":
    # You can change the limit here!
    run_triage_pipeline(limit=120)