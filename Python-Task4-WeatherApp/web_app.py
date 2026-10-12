"""
Smart Web Browser Launcher for Basic Weather App
Runs a local web server and opens the application in your default Web Browser.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os
import sys
import webbrowser
import weather_service

PORT = 5002
HOST = "0.0.0.0"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ Basic Weather App — Web Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f7fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-custom { border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: none; }
        .temp-display { font-size: 3.5rem; font-weight: 800; color: #1a202c; }
        .forecast-card { border-radius: 10px; background: #ffffff; border: 1px solid #e2e8f0; text-align: center; padding: 12px; }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 900px;">
        <div class="d-flex justify-content-between align-items-center mb-4 bg-white p-3 rounded shadow-sm">
            <div>
                <h3 class="fw-bold mb-0 text-primary">🌤️ BASIC WEATHER APP</h3>
                <small class="text-muted">Real-time Weather & Forecast Dashboard</small>
            </div>
            <div class="d-flex gap-2">
                <button id="btnAutoLoc" class="btn btn-outline-secondary">📍 Auto Location</button>
                <button id="btnToggleUnit" class="btn btn-purple btn-primary fw-bold">°C / °F</button>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="card card-custom p-4 bg-white mb-4">
            <div id="alertBox" class="alert alert-danger d-none mb-3"></div>
            <form id="searchForm">
                <div class="input-group input-group-lg">
                    <input type="text" id="cityInput" class="form-control" placeholder="Enter City Name or ZIP Code (e.g. London, Tokyo, 10001)" required>
                    <button type="submit" class="btn btn-primary fw-bold px-4">GET WEATHER</button>
                </div>
            </form>
        </div>

        <!-- Current Weather Hero Card -->
        <div class="card card-custom p-4 bg-white mb-4">
            <div class="row align-items-center">
                <div class="col-md-7">
                    <h2 id="resCity" class="fw-bold text-primary mb-1">Search a location above...</h2>
                    <div id="resTemp" class="temp-display">--°C</div>
                    <h4 id="resCond" class="text-secondary fw-semibold">Condition: —</h4>
                </div>
                <div class="col-md-5 text-md-end border-start border-light pt-3 pt-md-0">
                    <p id="resHumidity" class="fs-5 mb-2">💧 Humidity: —%</p>
                    <p id="resWind" class="fs-5 mb-2">💨 Wind Speed: —</p>
                    <p id="resSource" class="text-muted small mb-0">📡 Source: —</p>
                </div>
            </div>
        </div>

        <!-- Hourly Forecast (Next 6 Hours) -->
        <div class="card card-custom p-4 bg-white mb-4">
            <h5 class="fw-bold text-secondary mb-3">🕒 6-Hour Hourly Forecast</h5>
            <div class="row g-2" id="hourlyRow">
                <div class="col-12 text-center text-muted">No forecast data loaded.</div>
            </div>
        </div>

        <!-- Daily Forecast (Next 5 Days) -->
        <div class="card card-custom p-4 bg-white">
            <h5 class="fw-bold text-secondary mb-3">📅 5-Day Daily Forecast</h5>
            <div class="row g-2" id="dailyRow">
                <div class="col-12 text-center text-muted">No forecast data loaded.</div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentData = null;
        let isMetric = true;

        const form = document.getElementById('searchForm');
        const alertBox = document.getElementById('alertBox');
        const cityInput = document.getElementById('cityInput');

        async function fetchWeather(city) {
            alertBox.classList.add('d-none');
            const res = await fetch('/api/weather?city=' + encodeURIComponent(city));
            const data = await res.json();
            if (!data.success) {
                alertBox.textContent = data.message;
                alertBox.classList.remove('d-none');
                return;
            }
            currentData = data.data;
            renderWeather();
        }

        function renderWeather() {
            if (!currentData) return;
            const d = currentData;
            const unitStr = isMetric ? '°C' : '°F';

            document.getElementById('resCity').textContent = d.city + (d.country ? ', ' + d.country : '');
            const tempVal = isMetric ? d.temp_c : d.temp_f;
            document.getElementById('resTemp').textContent = tempVal.toFixed(1) + ' ' + unitStr;
            document.getElementById('resCond').textContent = d.icon + ' ' + d.condition;
            document.getElementById('resHumidity').textContent = '💧 Humidity: ' + d.humidity + '%';

            const windVal = isMetric ? (d.wind_speed_kmh + ' km/h') : (d.wind_speed_mph + ' mph');
            document.getElementById('resWind').textContent = '💨 Wind Speed: ' + windVal;
            document.getElementById('resSource').textContent = '📡 Source: ' + d.source;

            // Hourly Cards
            const hRow = document.getElementById('hourlyRow');
            hRow.innerHTML = '';
            (d.hourly || []).forEach(h => {
                const hTemp = isMetric ? h.temp_c : h.temp_f;
                hRow.innerHTML += `
                    <div class="col">
                        <div class="forecast-card">
                            <div class="fw-bold text-muted small">${h.time}</div>
                            <div class="fs-3 my-1">${h.icon}</div>
                            <div class="fw-bold">${hTemp.toFixed(1)}${unitStr}</div>
                        </div>
                    </div>
                `;
            });

            // Daily Cards
            const dRow = document.getElementById('dailyRow');
            dRow.innerHTML = '';
            (d.daily || []).forEach(dy => {
                const maxT = isMetric ? dy.temp_max_c : dy.temp_max_f;
                const minT = isMetric ? dy.temp_min_c : dy.temp_min_f;
                dRow.innerHTML += `
                    <div class="col">
                        <div class="forecast-card">
                            <div class="fw-bold text-primary">${dy.day}</div>
                            <div class="small text-muted">${dy.date.substring(5)}</div>
                            <div class="fs-2 my-1">${dy.icon}</div>
                            <div class="text-danger fw-bold small">Max ${maxT.toFixed(1)}${unitStr}</div>
                            <div class="text-primary small">Min ${minT.toFixed(1)}${unitStr}</div>
                            <div class="small text-secondary mt-1">${dy.condition}</div>
                        </div>
                    </div>
                `;
            });
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (cityInput.value.trim()) {
                fetchWeather(cityInput.value.trim());
            }
        });

        document.getElementById('btnToggleUnit').addEventListener('click', () => {
            isMetric = !isMetric;
            renderWeather();
        });

        document.getElementById('btnAutoLoc').addEventListener('click', async () => {
            const res = await fetch('/api/autolocation');
            const data = await res.json();
            if (data.success && data.city) {
                cityInput.value = data.city;
                fetchWeather(data.city);
            } else {
                alertBox.textContent = 'Could not auto-detect location. Please search manually.';
                alertBox.classList.remove('d-none');
            }
        });

        // Auto load on start
        document.getElementById('btnAutoLoc').click();
    </script>
</body>
</html>
"""

class WeatherRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif path == "/api/autolocation":
            success, loc = weather_service.auto_detect_location()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if success:
                self.wfile.write(json.dumps({"success": True, "city": loc["city"]}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"success": False, "message": str(loc)}).encode("utf-8"))

        elif path == "/api/weather":
            city = query.get("city", [""])[0]
            success, data = weather_service.get_weather(city)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if success:
                self.wfile.write(json.dumps({"success": True, "data": data}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"success": False, "message": str(data)}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

def main():
    url = f"http://localhost:{PORT}"
    print("==================================================")
    print("  Basic Weather App — Web Edition")
    print(f"  Server Running on: {url}")
    print("  Opening Browser automatically...")
    print("==================================================")
    sys.stdout.flush()

    try:
        webbrowser.open(url)
    except Exception:
        pass

    server = HTTPServer((HOST, PORT), WeatherRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down web server.")

if __name__ == "__main__":
    main()
