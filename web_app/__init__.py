from flask import Flask, render_template, request
import json
from app.meal_planner import generate_week_plan_varied
from app.meal_planner import generate_week_plan

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    calories = request.form.get("targetCalories", "").strip()
    diet     = (request.form.get("diet") or "").strip() or None
    exclude  = (request.form.get("exclude") or "").strip() or None

    wants_email = (request.form.get("wantsEmail") == "yes")
    user_email  = (request.form.get("email") or "").strip()

    # DO NOT pass timeframe here; meal_planner already uses "week"
    plan = generate_week_plan_varied(calories, diet, exclude)

    #plan = generate_week_plan(calories, diet, exclude)

    if plan is None:
        return "Upstream API failed. Please try again later.", 502

    # Always save plan.json so the email script can read it
    try:
        with open("plan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2)
    except Exception:
        pass  # non-fatal for web view

    # Try to email only if the user opted in and provided an email
    email_sent = False
    email_error = None
    if wants_email and user_email:
        try:
            # Import here so the app still runs even if sendgrid isn't installed
            from email_weekly import send_plan_csv
            send_plan_csv(user_email)
            email_sent = True
        except Exception as e:
            email_error = str(e)[:200]

            
    week = plan.get("week")
    if not week:
        # Show what came back so you can diagnose quickly
        shape = ", ".join(plan.keys())
        return f"No 'week' in response (got keys: {shape}).", 500

    day_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    labels = ["Breakfast", "Lunch", "Dinner"]

    return render_template(
        "results.html",
        week=week,
        day_order=day_order,
        labels=labels,
        calories=calories,
        diet=diet,
        exclude=exclude
    )

# optional: run directly (useful when not using FLASK_APP env)
if __name__ == "__main__":
    app.run(debug=True)