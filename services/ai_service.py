# services/ai_service.py
import ollama
import re
from config import OLLAMA_MODEL


def analyze_email_with_ollama(subject, body):
    # Context window ektu bariye 2500 korlam, HTML deep clean korar pore eta safe
    text_to_analyze = body[:2500]

    prompt = f"""
    Analyze the following email. 
    Subject: {subject}
    Body: {text_to_analyze}

    Provide your output in exactly this format:
    Actionable: [Yes/No]
    Summary: [A 2-line summary of the email]

    Rule 1: Newsletters, alerts, and marketing are NOT actionable.
    Rule 2: Do not include any other text in your response.
    """

    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])

        result = response['message']['content'].strip()

        # --- NEW: Smart Regex Parsing ---
        # Look for Actionable: Yes/No regardless of bolding or spaces
        action_match = re.search(r'Actionable\s*[:\*]*\s*(Yes|No)', result, re.IGNORECASE)
        actionable_part = action_match.group(1).capitalize() if action_match else "Check Manually"

        # Look for Summary: and grab everything after it
        summary_match = re.search(r'Summary\s*[:\*]*\s*(.*)', result, re.IGNORECASE | re.DOTALL)

        if summary_match:
            summary_part = summary_match.group(1).strip()
        else:
            # Fallback: If it completely forgot the label, just take the whole output
            summary_part = result.replace("Actionable: Yes", "").replace("Actionable: No", "").strip()
            if not summary_part:
                summary_part = "AI provided empty summary."

        return actionable_part, summary_part

    except Exception as e:
        print(f"Ollama Error: {e}")
        return "No", f"[AI Processing Failed: {str(e)}]"