from pathlib import Path
import sys
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Allow imports from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from snowflake.connection import get_connection


def get_high_risk_containers():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                container_id,
                location,
                risk_score,
                risk_level
            FROM ATMOSYNC.RAW.SPOILAGE_RISK
            WHERE UPPER(risk_level) = 'HIGH'
            ORDER BY risk_score DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def send_email_alert(containers):
    sender = os.getenv("ALERT_EMAIL_SENDER")
    password = os.getenv("ALERT_EMAIL_PASSWORD")
    receiver = os.getenv("ALERT_EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("Email alert skipped: email configuration is missing.")
        return

    message = EmailMessage()
    message["Subject"] = "AtmoSync High-Risk Container Alert"
    message["From"] = sender
    message["To"] = receiver

    lines = [
        "AtmoSync High-Risk Container Alert",
        "",
        f"High-risk containers detected: {len(containers)}",
        "",
    ]

    for container_id, location, risk_score, risk_level in containers:
        lines.append(
            f"Container: {container_id} | "
            f"Location: {location} | "
            f"Risk Score: {risk_score} | "
            f"Risk Level: {risk_level}"
        )

    message.set_content("\n".join(lines))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, password)
        smtp.send_message(message)

    print("Email alert sent successfully.")


if __name__ == "__main__":
    containers = get_high_risk_containers()

    print("\n===== AtmoSync High-Risk Container Alert =====")

    if not containers:
        print("No high-risk containers detected.")

    else:
        print(f"High-risk containers detected: {len(containers)}")

        for container_id, location, risk_score, risk_level in containers:
            print(
                f"Container: {container_id} | "
                f"Location: {location} | "
                f"Risk Score: {risk_score} | "
                f"Risk Level: {risk_level}"
            )

        send_email_alert(containers)
