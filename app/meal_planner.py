import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("SPOONACULAR_API_KEY")

# API url
url = "https://api.spoonacular.com/mealplanner/generate"

# User input for calories
calories = input("Enter target calories: ")

# Parameters
params = {
    "timeFrame": "day",
    "targetCalories": calories,
    "apiKey": API_KEY
}

# Fetch data
response = requests.get(url, params=params)
data = response.json()

print(data)