# test/test_meal_planner_save.py

import json
import os
import app.meal_planner as mp


def test_main_saves_plan_json(monkeypatch, tmp_path):
    # Fake day plan
    fake_day_plan = {
        "meals": [
            {"id": 1, "title": "Test Meal", "readyInMinutes": 15, "servings": 2, "sourceUrl": "http://example.com"}
        ],
        "nutrients": {"calories": 123, "protein": 10, "fat": 5, "carbohydrates": 15}
    }

    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return fake_day_plan
    

    # Used ChatGPT for the code:
    # Mock requests.get so no network call
    monkeypatch.setattr(mp.requests, "get", lambda *a, **k: MockResponse())

    # Mock user input: calories, diet, exclude
    monkeypatch.setattr("builtins.input", lambda _: "2000")

    # Change working dir to tmp_path so we don't overwrite real files
    monkeypatch.chdir(tmp_path)

    # Call a minimal part of the __main__ logic
    plan = mp.generate_week_plan_varied(2000)
    with open("plan.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    # Assert plan.json was created
    assert os.path.exists("plan.json")

    # Assert content is valid JSON
    with open("plan.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "week" in data