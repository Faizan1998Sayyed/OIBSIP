"""
CLI Application for Basic Weather App (Beginner Tier)
Interactive command-line interface with input validation, error handling, and unit displays.
"""

import weather_service

def prompt_bool(question: str, default: bool = True) -> bool:
    """Helper to prompt user for yes/no choice."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        choice = input(question + suffix).strip().lower()
        if not choice:
            return default
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def run_cli():
    print("==================================================")
    print("  🌤️ BASIC WEATHER APP (CLI Edition)")
    print("  Real-time weather data & forecasts")
    print("==================================================\n")

    api_key = input("Enter OpenWeatherMap API Key (Press ENTER to use Free Engine): ").strip()
    print()

    while True:
        city_input = input("Enter City Name or ZIP Code: ").strip()

        # 1. Input Validation: reject empty city input
        if not city_input:
            print("❌ Input Error: City name or ZIP code cannot be empty. Please try again.\n")
            continue

        print(f"Fetching weather data for '{city_input}'...")
        success, data = weather_service.get_weather(city_input, api_key=api_key)

        if not success:
            print(f"❌ Error: {data}\n")
        else:
            print("\n" + "=" * 55)
            print(f"  📍 LOCATION:      {data['city']}, {data['country']}")
            print(f"  🌡️ TEMPERATURE:   {data['temp_c']} °C  /  {data['temp_f']} °F")
            print(f"  ☁️ CONDITION:     {data['icon']} {data['condition']}")
            print(f"  💧 HUMIDITY:      {data['humidity']}%")
            print(f"  💨 WIND SPEED:    {data['wind_speed_kmh']} km/h ({data['wind_speed_mph']} mph)")
            print(f"  📡 DATA SOURCE:   {data['source']}")
            print("=" * 55)

            # Display 6-hour forecast summary
            if data.get('hourly'):
                print("\n  🕒 6-HOUR HOURLY FORECAST:")
                h_str = "  "
                for h in data['hourly']:
                    h_str += f"[{h['time']}: {h['temp_c']}°C {h['icon']}]  "
                print(h_str)

            # Display 5-day forecast summary
            if data.get('daily'):
                print("\n  📅 5-DAY DAILY FORECAST:")
                for d in data['daily']:
                    print(f"  • {d['day']} ({d['date']}): Max {d['temp_max_c']}°C / Min {d['temp_min_c']}°C  {d['icon']} {d['condition']}")
            print("\n")

        if not prompt_bool("Search another city?", default=True):
            print("\nThank you for using Basic Weather App! Goodbye 👋")
            break
        print("\n")


if __name__ == "__main__":
    run_cli()
