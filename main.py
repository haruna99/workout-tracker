import os
import requests
import datetime as dt

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

GENDER = "male"
WEIGHT_KG = "80"
HEIGHT_CM = "172"
AGE = "37"

exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0"
}

exercise_payload = {
    "query": input("Which exercises did you do: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=API_URL, headers=exercise_headers, json=exercise_payload)
exercise_response.raise_for_status()
exercises = exercise_response.json()["exercises"]

SHEETY_URL = "https://api.sheety.co/75b910ec42643eafc84fedae1ff65ac8/workoutTracking/workouts"
SHEETY_API_KEY = os.environ.get("SHEETY_API_KEY")

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_API_KEY}",
    "Content-Type": "application/json"
}

today = dt.datetime.now()
day = today.strftime("%d/%m/%Y")
time = today.strftime("%X")


for exercise in exercises:
    payload = {
        "workout": {
            "date": day,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    response = requests.post(url=SHEETY_URL, headers=sheety_headers, json=payload)
    response.raise_for_status()
    print(response.text)
