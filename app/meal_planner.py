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

# User input for calories
calories = input("Enter target calories: ").strip()
diet = input("Diet type (optional: vegetarian/vegan/keto/paleo/pescetarian): ").strip()
exclude = input("Exclude ingredients (optional, comma-separated e.g., peanuts,shellfish): ").strip()

# Parameters
params = {
    "timeFrame": "day",
    "targetCalories": calories,
    "apiKey": API_KEY
}

if diet:
    params["diet"] = diet
if exclude:
    params["exclude"] = exclude

# Fetch data
response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=2))

# Save raw JSON for later steps, this part is with the help of ChatGPT
with open("plan.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print("\nSaved to plan.json")

# Tiny console summary of meals
meals = data.get("meals", [])
totals = data.get("nutrients", {})
if totals:
    print("\n=== Daily Totals ===")
    print(f"Calories: {totals.get('calories')}")
    print(f"Protein:  {totals.get('protein')} g")
    print(f"Fat:      {totals.get('fat')} g")
    print(f"Carbs:    {totals.get('carbohydrates')} g")

if meals:
    labels = ["Breakfast", "Lunch", "Dinner"]
    print("\n=== Meals ===")
    for i, m in enumerate(meals[:3]):
        label = labels[i] if i < len(labels) else f"Meal {i+1}"
        print(f"{label}: {m.get('title')} • {m.get('readyInMinutes')} min")
        if m.get("sourceUrl"):
            print(f"  {m['sourceUrl']}")