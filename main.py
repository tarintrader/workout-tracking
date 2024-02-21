import requests
from datetime import *
import os

# ------------------------- NUTRITIONIX API ------------------------- #
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")



def get_workouts():
    exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    exercise_input = input("Tell me which exercise you did: ")

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
    }

    parameters = {
        "query": exercise_input
    }

    response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
    response.raise_for_status()
    print(response)
    workout_data = response.json()

    exercises_list = workout_data["exercises"]

    for exercise in exercises_list:
        global date, time, name, duration, calories
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        name = exercise["name"]
        duration = exercise["duration_min"]
        calories = exercise["nf_calories"]

        save_sheet()


# ------------------------- SHEETY API ------------------------- #
TOKEN = os.environ.get("TOKEN")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

def save_sheet():

    header = {
        "Content-Type": "application/json",
        "Authorization": TOKEN
    }

    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": name,
            "duration": duration,
            "calories": calories
        }
    }

    response = requests.post(url=SHEET_ENDPOINT, json=sheety_params, headers=header)
    response.raise_for_status()
    print(response)


get_workouts()