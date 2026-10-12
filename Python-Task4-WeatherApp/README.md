# 🌤️ Basic Weather App — OASIS INFOBYTE SIP

## OASIS INFOBYTE SIP Internship

* **Track:** Python Programming
* **Task:** Task 4 — Basic Weather App
* **Project Name:** Weather App
* **Target Path:** `OIBSIP/Python-Task4-WeatherApp/`
* **Intern Name:** Faizan Sayyed

---

A full-featured, submission-ready Python **Basic Weather App** supporting **Beginner CLI**, **Advanced Tkinter GUI**, and **Web Browser** modes.

Features a **Dual API Weather Engine** supporting both **OpenWeatherMap API** (with API key) and **Open-Meteo Free API** (requires **NO API Key**), ensuring the app works **100% out-of-the-box immediately**!

---

## ✨ Feature Checklist

### Beginner Tier (CLI)
- [x] **City / ZIP Input:** Prompt user to enter a city name or ZIP code.
- [x] **API Query & Parsing:** Make HTTP API calls and parse structured JSON weather data.
- [x] **Core Metrics Display:** Temperature in both °C and °F, humidity percentage, weather condition description, and wind speed.
- [x] **Graceful Error Handling:** Handles city not found (HTTP 404), network timeouts, invalid API keys (HTTP 401), and connection drops.
- [x] **Input Validation:** Rejects empty city inputs with clear warning messages.
- [x] **Continuous Loop:** Search another city without restarting the CLI program.

### Advanced Tier (Tkinter GUI & Web Browser)
- [x] **Modern GUI Window:** Tkinter GUI with city input field, "Get Weather" button, and card results panels.
- [x] **Visual Weather Icons:** Displays condition-matched visual icons (☀️ Clear, ⛅ Partly Cloudy, ☁️ Overcast, 🌧️ Rain, 🌩️ Snow, ⛈️ Thunderstorm).
- [x] **Hourly Forecast Panel:** Visual cards showing weather for the **next 6 hours**.
- [x] **Daily Forecast Panel:** Cards displaying weather for the **next 5 days** with High/Low temperatures.
- [x] **Unit Toggle Switch:** Instant **°C / °F** toggle button switching all temperature displays dynamically.
- [x] **Automatic Location Detection:** Detects user's current city via IP address using `ip-api.com` / `ipinfo.io`.
- [x] **Web Browser Edition:** Interactive web dashboard at `http://localhost:5002` via `python web_app.py`.

---

## 🛠️ Technologies Used

- **Language:** Python 3.12+
- **HTTP Client:** `requests`
- **GUI Framework:** `tkinter` & `ttk`
- **Weather APIs:** OpenWeatherMap API & Open-Meteo Free API (Zero key required)
- **Geolocation:** `ip-api.com` & `ipinfo.io` IP geocoding
- **Web Interface:** Python `http.server` + Bootstrap 5 HTML/CSS/JS

---

## 💻 Installation & Setup

1. Open PowerShell or Command Prompt in the project directory:
   ```cmd
   cd D:\Practice\weather_app
   ```

2. Install third-party requirements:
   ```cmd
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Application

### 1. Advanced Tkinter GUI Mode (Default)
```cmd
python main.py
```

### 2. Beginner CLI Mode
```cmd
python main.py --cli
```

### 3. Web Browser Mode
```cmd
python web_app.py
```
*Opens `http://localhost:5002` automatically in your web browser!*

---

## 🧪 Running Automated Unit Tests

To run the automated test suite verifying temperature conversions, geocoding fallback, and response parsing:

```cmd
python test_runner.py
```

Expected Output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 1.105s

OK
```

---

## 📁 Project Structure

```
Python-Task4-WeatherApp/
├── weather_service.py         # Dual API Weather Engine (OpenWeatherMap, Open-Meteo, Geocoding, IP location)
├── cli_app.py                 # Beginner Tier: Interactive CLI tool
├── gui_app.py                 # Advanced Tier: Tkinter GUI with 6-hr hourly & 5-day daily forecasts
├── main.py                    # Main launcher entry point (GUI default, --cli flag support)
├── web_app.py                 # Browser Edition (Bootstrap 5 Weather Dashboard on port 5002)
├── test_runner.py             # Automated unit test suite (5/5 passing)
├── requirements.txt           # Dependencies (requests, pillow)
├── README.md                  # Complete project documentation
└── .gitignore                 # Standard Python gitignore
```
