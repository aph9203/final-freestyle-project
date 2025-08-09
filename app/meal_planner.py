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
        print(f"API error: {response.status_code}")
        print(response.text[:500])
        return None
    return response.json()

# New Part for varied recommendation on different days
def generate_day_plan(calories, diet=None, exclude=None):
    """
    Get a single day's plan. Returns {"meals":[...], "nutrients": {...}}.
    """
    params = {
        "timeFrame": "day",
        "targetCalories": calories,
        "apiKey": API_KEY,
    }
    if diet:
        params["diet"] = diet
    if exclude:
        params["exclude"] = exclude

    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def generate_week_plan_varied(calories, diet=None, exclude=None):
    """
    Create a week by calling the day generator 7 times and try to avoid repeats.
    Shape matches the normal weekly payload: {"week": {monday: {...}, ...}}
    """
    day_names = ["monday", "tuesday", "wednesday",
                 "thursday", "friday", "saturday", "sunday"]

    seen_ids = set()
    week = {}

    for day in day_names:
        # try up to 4 attempts to get three unseen meals
        chosen = None
        for _ in range(4):
            d = generate_day_plan(calories, diet, exclude)
            meals = []
            for m in d.get("meals", [])[:3]:
                mid = m.get("id")
                if mid not in seen_ids:
                    meals.append(m)
                    seen_ids.add(mid)
            if len(meals) == 3:
                chosen = {"meals": meals, "nutrients": d.get("nutrients", {})}
                break

        # fallback: use whatever we got last if uniqueness failed
        if chosen is None:
            chosen = {"meals": d.get("meals", [])[:3], "nutrients": d.get("nutrients", {})}

        week[day] = chosen

    return {"week": week}





# User input for calories
if __name__ == "__main__":
    print("=== Minimal Meal Planner (Weekly) ===")
    calories = input("Enter target calories: ").strip()
    diet = input("Diet type (optional: vegetarian/vegan/keto/paleo/pescetarian): ").strip()
    exclude = input("Exclude ingredients (optional, comma-separated e.g., peanuts,shellfish): ").strip()

    plan = generate_week_plan_varied(calories, diet or None, exclude or None)

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