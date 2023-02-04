import json
import os
from dotenv import load_dotenv

import requests

load_dotenv()
calendarific_api_endpoint = "https://calendarific.com/api/v2/holidays?api_key="
calendarific_api_key = os.getenv("CALENDARIFIC_API_KEY")

msia_holidays = {}

# Get all holidays for Malaysia
def get_msia_holidays():
    print("calendarific_api_key: ", calendarific_api_key)
    response = requests.get(calendarific_api_endpoint +
                            calendarific_api_key + "&country=MY&year=2022")
    data = json.loads(response.text)
    calendarific_holidays = data['response']['holidays']

    for holiday in calendarific_holidays:
        name = holiday['name']
        # get date
        date = holiday['date']['iso']

        msia_holidays[date] = name

    with open('msia_holidays.json', 'w') as f:
        json.dump(msia_holidays, f)


get_msia_holidays()
