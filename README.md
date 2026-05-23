# Spam Mail Classifier and Gmail Triage Assistant

A Python based Gmail mail extraction, spam checking, and mail triage project. The repository contains two related workflows. The first workflow reads Gmail messages through IMAP, extracts readable content from mail body, images, and document attachments, analyzes the mail with a local Ollama model, and saves the final triage result to Google Sheets. The second workflow extracts unread Gmail messages, stores them in JSON format, and displays them through a small Flask web interface.

## Project Overview

The project is designed to help users process incoming Gmail messages automatically. It can collect sender information, subject, date, plain text body, cleaned HTML body, image OCR text, and text from attached PDF or Word documents. After collecting the mail content, the project can use a local Ollama model to generate a short summary and identify whether the message is actionable.

Although the repository name suggests a spam classifier, the current codebase works more like a Gmail extraction and triage assistant. A simple rule based spam check is also present in the Gmail extraction workflow.

## Main Objectives

1. Extract latest or unread Gmail messages automatically.
2. Clean HTML mail content and preserve useful text.
3. Extract useful links from newsletter style messages.
4. Read text from image attachments using OCR.
5. Read text from PDF and Word attachments.
6. Analyze mail content using a local Ollama model.
7. Store triage output in Google Sheets.
8. Save extracted mail content into a local JSON file.
9. Display extracted mail data through a Flask interface.
10. Support browser based Gmail extraction using Playwright.

## Features

### Gmail Extraction

1. Connects to Gmail through IMAP.
2. Fetches latest messages from the inbox.
3. Fetches unread messages and marks them as read when processed.
4. Extracts sender, subject, date, and mail body.
5. Handles both plain text and HTML mail formats.
6. Cleans HTML content using BeautifulSoup.
7. Extracts useful links from HTML messages.

### OCR Support

1. Detects image attachments inside mail messages.
2. Reads image files using Pillow.
3. Extracts text from images using Tesseract OCR.
4. Adds extracted OCR content to the final mail context.

### Document Attachment Support

1. Detects PDF, DOCX, and DOC attachments.
2. Extracts PDF text using PyPDF2.
3. Extracts Word document text using python docx.
4. Adds attachment text to the final analysis context.

### AI Based Mail Triage

1. Sends cleaned mail content to a local Ollama model.
2. Generates a short two line mail summary.
3. Predicts whether the mail is actionable.
4. Uses regex based parsing to handle model output.
5. Falls back to manual checking when the response format is unclear.

### Google Sheets Export

1. Connects to Google Sheets through a service account.
2. Creates headers when the target sheet is empty.
3. Avoids duplicate rows using subject and date signature.
4. Appends extracted mail results in batch mode.
5. Stores sender, date, subject, context, summary, and actionable status.

### Flask Mail Viewer

1. Reads extracted mail content from `data.json`.
2. Renders mail data in a web page.
3. Shows sender, subject, date, and body.
4. Displays an empty state when no extracted data is available.

### Playwright Gmail Automation

1. Opens Gmail in a real Chrome browser.
2. Uses persistent browser profile for manual login.
3. Supports Playwright inspector based object capture.
4. Includes pytest based Gmail inbox extraction flow.
5. Saves extracted unread mail data into `data.json`.

## Repository Structure

```text
spam_mail_classifier_git/
    main.py
    config.py
    requirements.txt
    LICENSE

    services/
        __init__.py
        ai_service.py
        document_service.py
        email_service.py
        ocr_service.py
        sheets_service.py

    spam_classifier/
        app.py
        bypass.py
        cookies.json
        data.json
        fetch_emails.py
        gmail_login.py
        hook_codegen.py
        pytest.ini
        record_gmail.py

        pages/
            __init__.py
            gmail_inbox_page.py

        templates/
            index.html

        tests/
            conftest.py
            test_extract_emails.py
```

## Workflow

### Root Triage Pipeline

```text
Gmail inbox
    IMAP mail fetch
        Mail body extraction
            HTML cleaning
            Link extraction
            Image OCR
            PDF and Word text extraction
                Combined mail context
                    Ollama analysis
                        Actionable status and summary
                            Google Sheets export
```

### Local Mail Viewer Workflow

```text
Unread Gmail messages
    IMAP extraction or Playwright extraction
        Cleaned mail data
            data.json
                Flask web interface
```

## Tech Stack

| Area | Technology |
| :-- | :-- |
| Language | Python |
| Mail access | IMAP |
| Browser automation | Playwright |
| Browser test runner | pytest |
| Web interface | Flask |
| HTML parsing | BeautifulSoup |
| OCR | Tesseract OCR, pytesseract, Pillow |
| PDF parsing | PyPDF2 |
| Word parsing | python docx |
| AI analysis | Ollama |
| Spreadsheet export | Google Sheets API, gspread |
| Authentication support | Gmail app password, Google service account |

## Prerequisites

Before running this project, make sure the following tools are available.

1. Python 3.10 or higher.
2. Google account with Gmail access.
3. Gmail app password for IMAP access.
4. Google Sheets service account credentials for Sheets export.
5. Tesseract OCR installed on the machine.
6. Ollama installed locally.
7. A downloaded Ollama model, for example `llama3.2`.
8. Chrome browser, if Playwright Gmail automation is used.

## Installation

Clone the repository.

```bash
git clone https://github.com/mirazchowdhury/spam_mail_classifier_git.git
cd spam_mail_classifier_git
```

Create and activate a virtual environment.

```bash
python -m venv .venv
```

For Windows:

```bash
.venv\Scripts\activate
```

For Linux or macOS:

```bash
source .venv/bin/activate
```

Install the packages from the repository.

```bash
pip install -r requirements.txt
```

The current `requirements.txt` mainly covers Playwright and pytest related packages. For the full triage pipeline, install the extra packages below.

```bash
pip install flask beautifulsoup4 html2text gspread oauth2client PyPDF2 python-docx pytesseract pillow ollama seleniumbase playwright-stealth
```

Install Playwright browser support.

```bash
playwright install chromium
```

## Configuration

The project currently reads configuration from `config.py`.

Required values are:

| Variable | Purpose |
| :-- | :-- |
| `EMAIL_ACCOUNT` | Gmail address used for IMAP access |
| `APP_PASSWORD` | Gmail app password |
| `GOOGLE_SHEET_NAME` | Target Google Sheet name |
| `OLLAMA_MODEL` | Local Ollama model name |
| `TESSERACT_PATH` | Tesseract executable path |

Example safe configuration format:

```python
EMAIL_ACCOUNT = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"
GOOGLE_SHEET_NAME = "My Triage Sheet"
OLLAMA_MODEL = "llama3.2"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Important Security Notice

The current repository contains hardcoded mail credentials in Python files. Before using this project in a real account, revoke those exposed app passwords from Google account settings and create fresh credentials. Do not commit real passwords, app passwords, session cookies, or service account files to GitHub.

Recommended improvement:

1. Move secrets to a `.env` file.
2. Add `.env`, `credentials.json`, `cookies.json`, and generated profile folders to `.gitignore`.
3. Load secrets using `python-dotenv`.
4. Rotate any password that was ever pushed to a public repository.

Example `.env` structure:

```env
EMAIL_ACCOUNT=your_email@gmail.com
APP_PASSWORD=your_app_password
GOOGLE_SHEET_NAME=My Triage Sheet
OLLAMA_MODEL=llama3.2
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Google Sheets Setup

To use the Google Sheets export pipeline:

1. Create a project in Google Cloud Console.
2. Enable Google Sheets API and Google Drive API.
3. Create a service account.
4. Download the service account JSON file.
5. Rename the downloaded file as `credentials.json`.
6. Place `credentials.json` in the repository root.
7. Create a Google Sheet with the name used in `GOOGLE_SHEET_NAME`.
8. Share that Google Sheet with the service account email.

The pipeline creates the following sheet columns when the sheet is empty:

| Column | Description |
| :-- | :-- |
| Sender | Mail sender |
| Date | Mail date |
| Subject | Mail subject |
| Full Body | Cleaned text, OCR text, and attachment text |
| Summary and Links | AI generated mail summary |
| Actionable | Yes, No, or manual checking status |

## Tesseract OCR Setup

### Windows

Install Tesseract OCR and set the path in `config.py`.

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Linux

Install Tesseract.

```bash
sudo apt update
sudo apt install tesseract-ocr
```

Then update the path if needed.

```python
TESSERACT_PATH = "/usr/bin/tesseract"
```

## Ollama Setup

Install Ollama and pull a model.

```bash
ollama pull llama3.2
```

Make sure the model name matches `OLLAMA_MODEL`.

```python
OLLAMA_MODEL = "llama3.2"
```

## How to Run the Root Triage Pipeline

Run the main pipeline from the repository root.

```bash
python main.py
```

This will:

1. Connect to Gmail.
2. Fetch latest inbox messages.
3. Extract body text, image OCR text, and document attachment text.
4. Create a combined mail context.
5. Analyze the message using Ollama.
6. Save the result into Google Sheets.

You can change the number of fetched messages in `main.py`.

```python
run_triage_pipeline(limit=120)
```

## How to Run the Simple Gmail Extraction Script

Go to the `spam_classifier` folder.

```bash
cd spam_classifier
```

Run the extraction script.

```bash
python fetch_emails.py
```

This script:

1. Connects to Gmail through IMAP.
2. Finds unread messages.
3. Extracts sender, subject, date, and body.
4. Saves the extracted data into `data.json`.

## How to Run the Flask Mail Viewer

From the `spam_classifier` folder, run:

```bash
python app.py
```

Open the local server in your browser.

```text
http://127.0.0.1:5000
```

The page displays extracted mail data from `data.json`.

## How to Use Playwright Gmail Automation

### Record Gmail Session

Run:

```bash
python record_gmail.py
```

This opens Chrome with a persistent profile. Log in manually and use Playwright inspector to inspect Gmail elements.

### Browser Bypass Script

Run:

```bash
python bypass.py
```

This opens Gmail using a persistent Chrome context and stealth settings.

### Hook Playwright Inspector to Existing Chrome

Start Chrome with remote debugging enabled, then run:

```bash
python hook_codegen.py
```

This connects Playwright to the existing Chrome session and opens the inspector.

## Running Tests

Go to the `spam_classifier` folder.

```bash
cd spam_classifier
pytest
```

The pytest workflow opens Gmail through a browser context, loads saved cookies from `cookies.json`, extracts unread messages, and writes them into `data.json`.

## Data Output Format

The extracted mail data is saved in JSON format.

```json
[
    {
        "sender": "Example Sender",
        "date_time": "Mon, 1 Jan 2026 10:00:00 +0600",
        "subject": "Example Subject",
        "email_body": "Cleaned email body"
    }
]
```

The browser automation workflow may also add status and classification values.

```json
[
    {
        "sender": "Example Sender",
        "date_time": "Mon, 1 Jan 2026 10:00:00 +0600",
        "email_body": "Cleaned email body",
        "status": "Read",
        "classify": "Authentic"
    }
]
```

## Simple Spam Classification Logic

The current spam classification logic is rule based. It marks a mail as spam when selected keywords such as `offer` or `win` appear in the subject. Otherwise, it marks the mail as authentic.

This is useful as a starting point, but it is not a trained machine learning spam classifier yet.

Recommended future model options:

1. Naive Bayes with TF IDF features.
2. Logistic Regression with text vectorization.
3. Linear SVM for text classification.
4. Transformer based mail classification.
5. Fine tuned multilingual model for Bangla and English mail text.

## Limitations

1. Credentials are currently hardcoded in source files.
2. `requirements.txt` does not include every package required for the full pipeline.
3. The spam detection part is rule based, not ML based.
4. Gmail UI automation may break if Gmail changes its HTML structure.
5. Gmail browser automation depends on session cookies or manual login.
6. OCR quality depends on image quality and Tesseract setup.
7. PDF extraction may fail for scanned PDF files without OCR.
8. Google Sheets export requires correct service account setup.

## Recommended Improvements

1. Replace hardcoded credentials with environment variables.
2. Add a clean `.env.example` file.
3. Update `requirements.txt` with all required packages.
4. Separate IMAP extraction, AI analysis, and UI into separate modules.
5. Add structured logging.
6. Add better exception handling.
7. Add a trained spam classifier.
8. Add unit tests for HTML cleaning, OCR parsing, and AI response parsing.
9. Add Docker support for easier setup.
10. Add a Streamlit or React dashboard for mail triage results.

## Suggested Production Structure

```text
spam_mail_classifier_git/
    app/
        config/
        core/
        services/
        repositories/
        api/
        ui/
        tests/

    data/
    docs/
    scripts/
    requirements.txt
    README.md
```

This structure would make the project easier to maintain as it grows.

## License

This project is released under the MIT License.

## Author

Miraj Uddin Chowdhury

GitHub repository:

```text
https://github.com/mirazchowdhury/spam_mail_classifier_git
```
