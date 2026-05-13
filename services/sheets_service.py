import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_NAME


def setup_google_sheets():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

    # Insert headers if the sheet is completely empty
    if not sheet.row_values(1):
        sheet.insert_row(["Sender", "Date", "Subject", "Full Body (Text+OCR)", "Summary & Links", "Actionable?"], 1)

    # Get existing signatures for deduplication
    all_rows = sheet.get_all_values()
    existing_signatures = {f"{row[2]} | {row[1]}" for row in all_rows[1:] if len(row) >= 3}

    return sheet, existing_signatures


def append_batch_to_sheet(sheet, rows):
    """Eksathe shob notun row sheet-e update kora"""
    if rows:
        sheet.append_rows(rows)