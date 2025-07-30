import copy
import os
import re
import time
from datetime import datetime
from email.utils import parseaddr

import requests

URL = os.getenv("SHEET_LINK")
API_URL = "http://127.0.0.1:8000/push"
POLL_INTERVAL = 10


def clean_text(text):
    if not text:
        return ""
    # Remove unicode whitespace/control characters
    return re.sub(r"[\u200c\r\n]+", " ", text).strip()


def extract_details_from_body(body):
    details = {"amount": None, "date": None, "vpa": None}

    # Extract amount (e.g., Rs.30.00 or Rs. 30.00)
    amount_match = re.search(r"Rs\.?\s?([\d,]+\.\d{2})", body)
    if amount_match:
        details["amount"] = amount_match.group(1)

    # Extract date in DD-MM-YY format
    date_match = re.search(r"\b(\d{2}-\d{2}-\d{2})\b", body)
    if date_match:
        try:
            details["date"] = (
                datetime.strptime(date_match.group(1), "%d-%m-%y").date().isoformat()
            )
        except ValueError:
            pass

    # Extract VPA (e.g., gametheory.96169739@hdfcbank)
    vpa_match = re.search(r"\b([a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+)\b", body)
    if vpa_match:
        details["vpa"] = vpa_match.group(1)

    return details


def parse_row(row):
    # Extract name and email from "From" field
    name, email = parseaddr(row.get("From", ""))

    parsed = {
        "timestamp": row.get("Timestamp", ""),
        "email": email,
        "name": name,
        "subject": clean_text(row.get("Subject", "")),
        "body": clean_text(row.get("Body", "")),
        "status": row.get("Status", ""),
    }

    # Optional: convert timestamp to datetime object
    try:
        parsed["timestamp"] = datetime.fromisoformat(
            parsed["timestamp"].replace("Z", "+00:00")
        )
    except Exception:
        pass  # Keep original string if parsing fails

    return parsed


def poll_sheet():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        header = data["header"]
        new_rows = data["rows"]

        if new_rows:
            print(f"New rows ({len(new_rows)}):")
            for row in new_rows:
                row_dict = dict(zip(header, row))
                parsed = parse_row(row_dict)
                if parsed["email"] == os.getenv("EMAIL_TO_BE_CHECKED"):
                    details = extract_details_from_body(parsed["body"])
                    parsed["amount"] = details["amount"]
                    parsed["date"] = details["date"]
                    parsed["vpa"] = details["vpa"]
                else:
                    parsed["amount"] = None
                    parsed["date"] = None
                    parsed["vpa"] = None
                # Convert datetime to ISO string for JSON serialization
                parsed_to_send = copy.deepcopy(parsed)
                if isinstance(parsed_to_send.get("timestamp"), datetime):
                    parsed_to_send["timestamp"] = parsed_to_send[
                        "timestamp"
                    ].isoformat()

                print("Pushing:", parsed_to_send)
                try:
                    r = requests.post(API_URL, json=parsed_to_send)
                    print("API status code:", r.status_code)
                    print("API response text:", r.text)
                except Exception as api_err:
                    print("API error:", api_err)
        else:
            print("No new rows.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    while True:
        poll_sheet()
        time.sleep(POLL_INTERVAL)
