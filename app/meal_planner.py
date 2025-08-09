import os
import json
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("SPOONACULAR_API_KEY")

# API url
url = "https://api.spoonacular.com/mealplanner/generate"


# Parameters
"""
Return a weekly meal plan JSON from Spoonacular.
"""
def generate_week_plan(calories, diet=None, exclude=None):
    params = {
        "timeFrame": "week",
        "targetCalories": calories,
        "apiKey": API_KEY
    }

    if diet:
        params["diet"] = diet
    if exclude:
        params["exclude"] = exclude

    # Fetch data
    response = requests.get(url, params=params)
    if not response.ok:
        # show a helpful message and the first part of the body
        print(f"API error: {r.status_code}")
        print(r.text[:500])
        return None
    return response.json()

# User input for calories
if __name__ == "__main__":
    print("=== Minimal Meal Planner (Weekly) ===")
    calories = input("Enter target calories: ").strip()
    diet = input("Diet type (optional: vegetarian/vegan/keto/paleo/pescetarian): ").strip()
    exclude = input("Exclude ingredients (optional, comma-separated e.g., peanuts,shellfish): ").strip()

    plan = generate_week_plan(calories, diet or None, exclude or None)

    # Save raw JSON for later steps, this part is with the help of ChatGPT
    with open("plan.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    print("\nSaved to plan.json")

    # Tiny console summary of meals
    week = plan.get("week", {})
    if not week:
        print("No 'week' key in response. Here's the payload shape:")
        print(list(plan.keys()))
        raise SystemExit(1)


    day_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    labels = ["Breakfast", "Lunch", "Dinner"]

    for day in day_order:
            day_block = week.get(day)
            if not day_block:
                 continue

            print(f"\n=== {day.capitalize()} ===")
            
            meals = day_block.get("meals", [])

            print("=== Meals ===")

            for i, m in enumerate(meals[:3]):
                label = labels[i] if i < len(labels) else f"Meal {i+1}"
                print(f"{label}: {m.get('title')} • {m.get('readyInMinutes')} min")
                if m.get("sourceUrl"):
                    print(f"  {m['sourceUrl']}")

            totals = day_block.get("nutrients", {})
            if totals:
                print("\n=== Daily Totals ===")
                print(f"Calories: {totals.get('calories')}")
                print(f"Protein:  {totals.get('protein')} g")
                print(f"Fat:      {totals.get('fat')} g")
                print(f"Carbs:    {totals.get('carbohydrates')} g")
            print()