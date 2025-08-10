## Spoonacular Meal Planner

This is the first step of the project.
It fetches weekly meal plan from the Spoonacular API using calories, diet and excluded ingredients if any as input.
The API key is stored in a `.env` file for security.

## Setup

1. Configure secrets with .env

SPOONACULAR_API_KEY=your_api_key_here
SENDGRID_API_KEY=your_real_sendgrid_key_here

2. Create & activate an environment
```sh
conda create -n meal-env python=3.11 -y
conda activate meal-env
```

3. Install packages
```sh
pip install -r requirements.txt
```
4. Run test
```sh
pytest
```

## Web App

5. Run the Flask web app
```sh
export FLASK_APP=web_app
flask run
```
Open the browser at http://127.0.0.1:5000

6. In the Web App
Enter calories/diet/exclusions/email address (optional) and you’ll get a Weekly Meal Plan on the Web App and if opted in Email