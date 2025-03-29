
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() 
url = "https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us"

# get from www.hoyolab.com
# after login, get it from inspect element -> storage -> cookies
mhyuuid = os.getenv("mhyuuid")
cookie_token = os.getenv("cookie_token")
ltoken = os.getenv("ltoken")
ltuid = os.getenv("ltuid")
# account_id = os.getenv("account_id")

# get from checkin page link, access via checking button in HoYoLAB
# https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id={payload} <- this
payload = f'{{"act_id": "{os.getenv("payload")}" }}'

header = {"Cookie": f'{"_MHYUUID={mhyuuid}; mi18nLang=en-us; ltoken={ltoken}; ltuid={ltuid}; cookie_token={cookie_token};"}',
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
          "Origin": "https://act.hoyolab.com/",
          "Referer": "https://act.hoyolab.com/"
          }

response_decoded_json = requests.post(url,data=payload, headers=header)
response_json = response_decoded_json.json()

print(response_json)
