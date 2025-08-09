import os
import json
import csv
import io
import base64
from dotenv import load_dotenv

# SendGrid (same as class)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

#CSV builder
def plan_to_csv_text(plan_dict):
    """
    Convert plan.json to CSV text with columns:
    Day, Meal, Title, ReadyInMinutes, SourceUrl
    Works for weekly (preferred) or daily payloads.
    """
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Day", "Meal", "Title", "ReadyInMinutes", "SourceUrl"])

    labels = ["Breakfast", "Lunch", "Dinner"]

    if "week" in plan_dict:
        week = plan_dict["week"]
        day_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        for day in day_order:
            day_block = (week or {}).get(day) or {}
            meals = day_block.get("meals", [])
            for i, m in enumerate(meals[:3]):
                label = labels[i] if i < len(labels) else f"Meal {i+1}"
                w.writerow([
                    day.capitalize(),
                    label,
                    m.get("title", ""),
                    m.get("readyInMinutes", ""),
                    m.get("sourceUrl", ""),
                ])
    else:
        meals = plan_dict.get("meals", [])
        for i, m in enumerate(meals[:3]):
            label = labels[i] if i < len(labels) else f"Meal {i+1}"
            w.writerow([
                "Day",
                label,
                m.get("title", ""),
                m.get("readyInMinutes", ""),
                m.get("sourceUrl", ""),
            ])

    return buf.getvalue()

# ---- Load plan.json ----
with open("plan.json", "r", encoding="utf-8") as f:
    plan = json.load(f)

csv_text = plan_to_csv_text(plan)

# PREPARE MESSAGE
subject = "Your Weekly Meal Plan"
html_content = """
    <h2>Your Meal Plan</h2>
    <p>Attached is your meal plan as a CSV file.</p>
"""

client = SendGridAPIClient(SENDGRID_API_KEY)
message = Mail(
    from_email="apriyankah@gmail.com",
    to_emails="apriyankah12@gmail.com",
    subject=subject,
    html_content=html_content
)

# ATTACH CSV
encoded_csv = base64.b64encode(csv_text.encode("utf-8")).decode()

csvAttachment = Attachment(
    FileContent(encoded_csv),
    FileName("meal_plan.csv"),
    FileType("text/csv"),
    Disposition("attachment")
)

message.attachment = csvAttachment

# SEND MESSAGE
response = client.send(message)
print(response.status_code)
