from flask import Flask, render_template, request
from app.meal_planner import generate_week_plan  # <-- uses week by default

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    calories = request.form.get("targetCalories", "").strip()
    diet     = (request.form.get("diet") or "").strip() or None
    exclude  = (request.form.get("exclude") or "").strip() or None

    # DO NOT pass timeframe here; meal_planner already uses "week"
    plan = generate_week_plan(calories, diet, exclude)
    if plan is None:
        return "Upstream API failed. Please try again later.", 502

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