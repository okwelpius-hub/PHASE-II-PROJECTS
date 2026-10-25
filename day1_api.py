import requests

url = "https://restcountries.com/v3.1/name/Uganda"
params = {"fields": "name,capital,population,currencies"}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    countries = response.json()
    country = countries[0]

    name = country["name"]["common"]
    capital = country.get("capital", ["Unknown"])[0]
    population = country.get("population", "Unknown")
    currencies = country.get("currencies", {})
    currency = next(iter(currencies), "Unknown")

    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population}")
    print(f"Currency: {currency}")

except requests.RequestException as error:
    print(f"Request failed: {error}")
except (ValueError, KeyError, IndexError) as error:
    print(f"Could not read the country data: {error}")

weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": 0.3476,
    "longitude": 32.5825,
    "current": "temperature_2m,precipitation,wind_speed_10m",
    "timezone": "auto",
}

try:
    response = requests.get(weather_url, params=weather_params, timeout=10)
    response.raise_for_status()

    data = response.json()
    current = data["current"]
    units = data["current_units"]

    print("\nCurrent weather in Kampala:")
    print(f"Time: {current['time']}")
    print(f"Temperature: {current['temperature_2m']} {units['temperature_2m']}")
    print(f"Precipitation: {current['precipitation']} {units['precipitation']}")
    print(f"Wind speed: {current['wind_speed_10m']} {units['wind_speed_10m']}")
except requests.RequestException as error:
    print(f"Weather request failed: {error}")
except (ValueError, KeyError, TypeError) as error:
    print(f"Could not read the weather data: {error}")


# Exercise: 
print("-" * 100)

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"fields": "id,symbol,name,current_price,market_cap,price_change_percentage_24h", "vs_currency": "usd", "ids": "bitcoin,ethereum,ripple"}
    
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    coins = response.json()

    print("\nCryptocurrency Prices:")
    for coin in coins:
        print(f"{coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:.2f}")
except requests.RequestException as error:
    print(f"Request failed: {error}")
except (ValueError, KeyError, IndexError) as error:
    print(f"Could not read the cryptocurrency data: {error}")
