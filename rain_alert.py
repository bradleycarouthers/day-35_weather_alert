#   rain_alert.py
# Sends SMS msg when weather condition code is within certain threshold

import requests
from twilio.rest import Client
import secret

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = secret.MY_LAT
MY_LONG = secret.MY_LONG
YOUR_LAT = -0.225660
YOUR_LONG = 100.634132
api_key = secret.api_key

account_sid = secret.account_sid
auth_token = secret.auth_token
from_number = secret.from_number

parameters = {
    "lat": YOUR_LAT,
    "lon": YOUR_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_code = weather_data['hourly'][0]['weather'][0]['id']

# Will it rain in the next 12 hours
will_rain = False
print("-" * 44)
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]['id']
    if int(condition_code) < 700:
        will_rain = True

# If conditions for raining is true, send SMS
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Celly, here! Don't forget your umbrella, my beloved user☔!",
        from_=from_number,
        to=secret.MY_NUMBER,
    )
    print(message.status)
