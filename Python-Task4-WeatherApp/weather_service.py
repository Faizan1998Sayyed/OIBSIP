"""
Weather Service Module for Basic Weather App
Handles API calls to OpenWeatherMap and Open-Meteo (Free Fallback, zero API key required),
IP-based auto location detection, unit conversions, and normalized weather response parsing.
"""

import requests
import json
from typing import Tuple, Dict, Any, List

def celsius_to_fahrenheit(c_temp: float) -> float:
    """Converts Celsius to Fahrenheit rounded to 1 decimal place."""
    return round((c_temp * 9 / 5) + 32, 1)

def fahrenheit_to_celsius(f_temp: float) -> float:
    """Converts Fahrenheit to Celsius rounded to 1 decimal place."""
    return round((f_temp - 32) * 5 / 9, 1)

def WMO_CODE_MAP(code: int) -> Tuple[str, str]:
    """Maps WMO Weather Interpretation Codes to condition description and emoji icon."""
    mapping = {
        0: ("Clear Sky", "☀️"),
        1: ("Mainly Clear", "🌤️"),
        2: ("Partly Cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Depositing Rime Fog", "🌫️"),
        51: ("Light Drizzle", "🌦️"),
        53: ("Moderate Drizzle", "🌦️"),
        55: ("Dense Drizzle", "🌧️"),
        61: ("Slight Rain", "🌧️"),
        63: ("Moderate Rain", "🌧️"),
        65: ("Heavy Rain", "🌧️"),
        71: ("Slight Snow", "🌨️"),
        73: ("Moderate Snow", "🌨️"),
        75: ("Heavy Snow", "❄️"),
        80: ("Rain Showers", "🌦️"),
        81: ("Moderate Rain Showers", "🌧️"),
        82: ("Violent Rain Showers", "⛈️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with Light Hail", "⛈️"),
        99: ("Thunderstorm with Heavy Hail", "⛈️")
    }
    return mapping.get(code, ("Cloudy", "☁️"))


def auto_detect_location() -> Tuple[bool, Dict[str, Any] | str]:
    """
    Detects user's current city and coordinates based on IP address via ip-api.com.
    """
    try:
        resp = requests.get("http://ip-api.com/json/", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                return True, {
                    "city": data.get("city", "Unknown"),
                    "country": data.get("countryCode", ""),
                    "lat": data.get("lat"),
                    "lon": data.get("lon")
                }
        # Secondary fallback
        resp2 = requests.get("https://ipinfo.io/json", timeout=5)
        if resp2.status_code == 200:
            data2 = resp2.json()
            loc = data2.get("loc", "").split(",")
            return True, {
                "city": data2.get("city", "Unknown"),
                "country": data2.get("country", ""),
                "lat": float(loc[0]) if len(loc) == 2 else 0.0,
                "lon": float(loc[1]) if len(loc) == 2 else 0.0
            }
    except Exception as e:
        return False, f"Could not auto-detect location: {str(e)}"
    
    return False, "Failed to resolve IP location."


def get_weather_openmeteo(lat: float, lon: float, city_name: str, country_code: str = "") -> Tuple[bool, Dict[str, Any] | str]:
    """
    Fetches real-time weather and forecast data from Open-Meteo (Free, NO API Key needed).
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true&"
            f"hourly=temperature_2m,relative_humidity_2m,weathercode,windspeed_10m&"
            f"daily=weathercode,temperature_2m_max,temperature_2m_min&"
            f"timezone=auto"
        )
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return False, f"Open-Meteo API returned status code {resp.status_code}."

        data = resp.json()
        curr = data.get("current_weather", {})
        temp_c = curr.get("temperature", 0.0)
        temp_f = celsius_to_fahrenheit(temp_c)
        code = curr.get("weathercode", 0)
        condition, icon = WMO_CODE_MAP(code)
        wind_kmh = curr.get("windspeed", 0.0)
        wind_mph = round(wind_kmh * 0.621371, 1)

        # Parse Hourly Forecast (next 6 hours)
        hourly_list = []
        hourly_raw = data.get("hourly", {})
        times = hourly_raw.get("time", [])
        temps = hourly_raw.get("temperature_2m", [])
        codes = hourly_raw.get("weathercode", [])
        hids = hourly_raw.get("relative_humidity_2m", [])

        current_humidity = hids[0] if hids else 50

        for i in range(min(6, len(times))):
            t_str = times[i][-5:] if len(times[i]) >= 5 else times[i]
            t_c = temps[i] if i < len(temps) else temp_c
            t_f = celsius_to_fahrenheit(t_c)
            c_code = codes[i] if i < len(codes) else 0
            h_cond, h_icon = WMO_CODE_MAP(c_code)
            hourly_list.append({
                "time": t_str,
                "temp_c": t_c,
                "temp_f": t_f,
                "condition": h_cond,
                "icon": h_icon
            })

        # Parse Daily Forecast (next 5 days)
        daily_list = []
        daily_raw = data.get("daily", {})
        d_times = daily_raw.get("time", [])
        d_maxs = daily_raw.get("temperature_2m_max", [])
        d_mins = daily_raw.get("temperature_2m_min", [])
        d_codes = daily_raw.get("weathercode", [])

        import datetime
        for i in range(min(5, len(d_times))):
            d_str = d_times[i]
            try:
                dt_obj = datetime.datetime.strptime(d_str, "%Y-%m-%d")
                day_name = dt_obj.strftime("%a") # e.g. Mon, Tue
            except Exception:
                day_name = d_str

            max_c = d_maxs[i] if i < len(d_maxs) else temp_c
            min_c = d_mins[i] if i < len(d_mins) else temp_c
            dc = d_codes[i] if i < len(d_codes) else 0
            d_cond, d_icon = WMO_CODE_MAP(dc)

            daily_list.append({
                "day": day_name,
                "date": d_str,
                "temp_max_c": max_c,
                "temp_min_c": min_c,
                "temp_max_f": celsius_to_fahrenheit(max_c),
                "temp_min_f": celsius_to_fahrenheit(min_c),
                "condition": d_cond,
                "icon": d_icon
            })

        parsed_data = {
            "city": city_name,
            "country": country_code,
            "lat": lat,
            "lon": lon,
            "temp_c": temp_c,
            "temp_f": temp_f,
            "humidity": current_humidity,
            "condition": condition,
            "wind_speed_kmh": wind_kmh,
            "wind_speed_mph": wind_mph,
            "icon": icon,
            "hourly": hourly_list,
            "daily": daily_list,
            "source": "Open-Meteo Free API"
        }
        return True, parsed_data

    except requests.exceptions.Timeout:
        return False, "Network timeout while connecting to weather service."
    except requests.exceptions.ConnectionError:
        return False, "Network error. Please check your internet connection."
    except Exception as e:
        return False, f"Weather data processing error: {str(e)}"


def get_weather_openweathermap(city: str, api_key: str) -> Tuple[bool, Dict[str, Any] | str]:
    """
    Fetches real-time weather from OpenWeatherMap API using provided API key.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 404:
            return False, f"City '{city}' not found. Please check spelling."
        if resp.status_code == 401:
            return False, "Invalid OpenWeatherMap API key provided."
        if resp.status_code != 200:
            return False, f"OpenWeatherMap returned status code {resp.status_code}."

        data = resp.json()
        temp_c = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]
        wind_ms = data["wind"]["speed"]
        wind_kmh = round(wind_ms * 3.6, 1)

        city_name = data.get("name", city)
        country_code = data.get("sys", {}).get("country", "")
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # Fetch 5 day / 3 hour forecast for hourly and daily
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        f_resp = requests.get(forecast_url, timeout=8)
        hourly_list = []
        daily_list = []

        if f_resp.status_code == 200:
            fdata = f_resp.json()
            flist = fdata.get("list", [])
            # Next 6 intervals for hourly
            for item in flist[:6]:
                dt_txt = item.get("dt_txt", "")
                t_str = dt_txt[-8:-3] if len(dt_txt) >= 8 else dt_txt
                t_c = item["main"]["temp"]
                h_cond = item["weather"][0]["description"].title()
                hourly_list.append({
                    "time": t_str,
                    "temp_c": t_c,
                    "temp_f": celsius_to_fahrenheit(t_c),
                    "condition": h_cond,
                    "icon": "🌤️"
                })

            # Daily grouping
            days_seen = set()
            import datetime
            for item in flist:
                dt_txt = item.get("dt_txt", "")
                date_part = dt_txt.split(" ")[0] if " " in dt_txt else dt_txt
                if date_part not in days_seen:
                    days_seen.add(date_part)
                    try:
                        dt_obj = datetime.datetime.strptime(date_part, "%Y-%m-%d")
                        day_name = dt_obj.strftime("%a")
                    except Exception:
                        day_name = date_part

                    max_c = item["main"]["temp_max"]
                    min_c = item["main"]["temp_min"]
                    d_cond = item["weather"][0]["description"].title()
                    daily_list.append({
                        "day": day_name,
                        "date": date_part,
                        "temp_max_c": max_c,
                        "temp_min_c": min_c,
                        "temp_max_f": celsius_to_fahrenheit(max_c),
                        "temp_min_f": celsius_to_fahrenheit(min_c),
                        "condition": d_cond,
                        "icon": "🌤️"
                    })
                    if len(daily_list) >= 5:
                        break

        parsed_data = {
            "city": city_name,
            "country": country_code,
            "lat": lat,
            "lon": lon,
            "temp_c": temp_c,
            "temp_f": celsius_to_fahrenheit(temp_c),
            "humidity": humidity,
            "condition": condition,
            "wind_speed_kmh": wind_kmh,
            "wind_speed_mph": round(wind_kmh * 0.621371, 1),
            "icon": "🌤️",
            "hourly": hourly_list,
            "daily": daily_list,
            "source": "OpenWeatherMap API"
        }
        return True, parsed_data

    except requests.exceptions.Timeout:
        return False, "Network timeout while connecting to OpenWeatherMap."
    except requests.exceptions.ConnectionError:
        return False, "Network connection error."
    except Exception as e:
        return False, f"API Error: {str(e)}"


def get_weather(query: str, api_key: str = None) -> Tuple[bool, Dict[str, Any] | str]:
    """
    Main Weather Query Function.
    1. Validates non-empty query.
    2. Uses OpenWeatherMap API if api_key provided.
    3. Uses Geocoding + Open-Meteo Free API fallback if no key provided.
    """
    if not query or not query.strip():
        return False, "Please enter a valid city name or ZIP code."

    clean_query = query.strip()

    # If OpenWeatherMap API key supplied, use OpenWeatherMap
    if api_key and api_key.strip():
        return get_weather_openweathermap(clean_query, api_key.strip())

    # Fallback to Open-Meteo Geocoding + Weather API
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_query}&count=1&language=en&format=json"
        g_resp = requests.get(geo_url, timeout=8)
        if g_resp.status_code == 200:
            g_data = g_resp.json()
            results = g_data.get("results")
            if results and len(results) > 0:
                first = results[0]
                city_name = first.get("name", clean_query)
                country_code = first.get("country_code", "").upper()
                lat = first.get("latitude")
                lon = first.get("longitude")
                return get_weather_openmeteo(lat, lon, city_name, country_code)

        return False, f"City or ZIP code '{clean_query}' not found. Please check spelling."

    except requests.exceptions.Timeout:
        return False, "Network timeout during geocoding search."
    except requests.exceptions.ConnectionError:
        return False, "Network connection error. Please check your internet connection."
    except Exception as e:
        return False, f"Weather search error: {str(e)}"
