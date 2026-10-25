import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("OPENWEATHER_API_KEY is missing from the environment.")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Weather API request failed: {error}")
    except ValueError:
        print("Weather API returned invalid JSON.")
    return None


def get_country_info(country_code):
    country_api_key = os.getenv("REST_COUNTRIES_API_KEY")
    if not country_api_key:
        print("REST_COUNTRIES_API_KEY is missing from the environment.")
        return None

    url = f"https://api.restcountries.com/countries/v5/codes.alpha_2/{country_code}"
    headers = {"Authorization": country_api_key}
    params = {"response_fields": "names.common,region,population,currencies"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        countries = result.get("data", {}).get("objects", [])
        if countries:
            return countries[0]
        print(f"No country data found for country code '{country_code}'.")
    except requests.RequestException as error:
        print(f"Country API request failed: {error}")
    except (ValueError, AttributeError):
        print("Country API returned invalid or unexpected JSON.")
    return None


def save_to_file(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Weather data saved to {filename}")
    except OSError as error:
        print(f"Could not save weather data: {error}")


def run_tool():
    print("Travel Weather Tool")
    print("-------------------")
    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")
    weather_data = get_weather(city)
    if not weather_data:
        print(f"Could not retrieve weather data for '{city}'.")
        return

    try:
        country_code = weather_data["sys"]["country"]
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
    except (KeyError, IndexError, TypeError):
        print("Weather API response is missing expected data.")
        return

    country_data = get_country_info(country_code)

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {temperature} C")
    print(f"Condition   : {description.title()}")
    print(f"Humidity    : {humidity}%")
    print(f"Wind        : {wind_speed} m/s")

    if country_data:
        population = country_data.get("population", 0)
        region = country_data.get("region", "Unknown")
        currencies = ", ".join(
            currency.get("code", "Unknown")
            for currency in country_data.get("currencies", [])
        ) or "Unknown"
        country_name = country_data.get("names", {}).get("common", country_code)
        print("\n=== Country Info ===")
        print(f"Country     : {country_name}")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")

    filename = f"{city.lower().replace(' ', '_')}_weather.json"
    save_to_file(weather_data, filename)


if __name__ == "__main__":
    run_tool()

import json

with open("Kampala_weather.json", "r") as f:
    data = json.load(f)

print(data["main"]["temp"])