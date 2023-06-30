
import requests
import time
import random
import json
import os
from dotenv import load_dotenv


url = "https://hk4e-api-os.mihoyo.com/event/sol/sign?lang=en-us"

# get from cookies
mhyuuid = os.getenv("mhyuuid")

# get from https://hk4e-api-os.mihoyo.com/event/sol/info?lang=en-us
account_id = os.getenv("account_id")
cookie_token = os.getenv("cookie_token")
ltoken = os.getenv("ltoken")
ltuid = os.getenv("ltuid")

# get from checkin page
payload = f'{{"act_id": "{os.getenv("payload")}" }}'

header = {"Cookie": f"ltuid={ltuid}; ltoken={ltoken}; account_id={account_id}; cookie_token={cookie_token}; mhyuuid={mhyuuid};",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
          "Origin": "https://webstatic-sea.mihoyo.com",
          "Referer": "https://webstatic-sea.mihoyo.com/"
          }
#time.sleep(random.randint(1, 120))
response_decoded_json = requests.post(url, data=payload, headers=header)
response_json = response_decoded_json.json()


print(response_json)
