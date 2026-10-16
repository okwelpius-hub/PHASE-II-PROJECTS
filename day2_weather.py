import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Mbale"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    print(f"Weather in {city}")
    print(f"Temperature: {temp}°C")
    print(f"Condition: {description}")
    print(f"Humidity: {humidity}%")
else:
    print(f"Error: {response.status_code} - {response.text}")

print("-" * 50)
# Error Handling
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Mbale"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    print(f"Weather in {city}: {temp}C, {description}, humidity {humidity}%")

elif response.status_code == 401:
    print("API key is invalid or not yet active. Check your .env file.")

elif response.status_code == 404:
    print(f"City not found: {city}. Check the spelling.")

elif response.status_code == 429:
    print("Too many requests. Wait before trying again.")

else:
    print(f"Unexpected error: {response.status_code}")
    print(response.text)

print("-" * 50)
# Test 1

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("EXCHANGE_RATE_API_KEY")
rate = "Dollar to Shillings"

url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/UGX"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    conversion_rate = data["conversion_rate"]
    print(f"Exchange rate for {rate}: {conversion_rate} UGX")

elif response.status_code == 401:
    print("API key is invalid or not yet active. Check your .env file.")

elif response.status_code == 404:
    print(f"Currency pair not found. Check the currency codes.")

elif response.status_code == 429:
    print("Too many requests. Wait before trying again.")

else:
    print(f"Unexpected error: {response.status_code}")
    print(response.text)

