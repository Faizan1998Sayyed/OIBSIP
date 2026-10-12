"""
Smart BMI Calculator — Web Edition Launcher
Runs a local web server and opens the application in your default Web Browser.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os
import sys
import io
import webbrowser

import matplotlib
matplotlib.use('Agg') # Non-interactive backend for web rendering
import matplotlib.pyplot as plt

import bmi_logic
import database

PORT = 5000
HOST = "0.0.0.0" # Listen on all IPv4 interfaces

# Ensure DB initialized
database.init_db()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart BMI Calculator — Web Edition</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f7fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-custom { border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: none; }
        .badge-underweight { background-color: #3182CE; color: white; }
        .badge-normal { background-color: #38A169; color: white; }
        .badge-overweight { background-color: #DD6B20; color: white; }
        .badge-obese { background-color: #E53E3E; color: white; }
        .result-box { border-radius: 10px; padding: 20px; text-align: center; }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 950px;">
        <div class="d-flex justify-content-between align-items-center mb-4 bg-white p-3 rounded shadow-sm">
            <div>
                <h2 class="fw-bold mb-0 text-primary">SMART BMI CALCULATOR</h2>
                <small class="text-muted">OASIS INFOBYTE SIP — Task 2 (Web Edition)</small>
            </div>
            <span class="badge bg-success fs-6">🌐 Browser Edition Active</span>
        </div>

        <div class="row g-4">
            <!-- Left Column: Input Form -->
            <div class="col-md-6">
                <div class="card card-custom p-4 bg-white">
                    <h4 class="fw-bold mb-3 text-secondary">User Details</h4>
                    <div id="alertBox" class="alert alert-danger d-none"></div>
                    
                    <form id="bmiForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold">User Name</label>
                            <input type="text" id="userName" class="form-control form-control-lg" placeholder="e.g. Faizan" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Weight (kg)</label>
                            <input type="number" step="0.1" id="weight" class="form-control form-control-lg" placeholder="e.g. 70" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Height (meters)</label>
                            <input type="number" step="0.01" id="height" class="form-control form-control-lg" placeholder="e.g. 1.75" required>
                        </div>

                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-primary btn-lg fw-bold">CALCULATE & SAVE BMI</button>
                            <button type="button" id="btnClear" class="btn btn-outline-secondary">Clear Fields</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right Column: Result Panel -->
            <div class="col-md-6">
                <div class="card card-custom p-4 bg-white h-100 d-flex flex-column justify-content-between">
                    <div>
                        <h4 class="fw-bold mb-3 text-secondary">Calculation Result</h4>
                        <div id="resultBox" class="result-box bg-light text-muted">
                            <h5 id="resUser" class="mb-2">User: —</h5>
                            <h1 id="resBmi" class="display-4 fw-bold my-3">BMI: --.--</h1>
                            <h4 id="resCategory" class="mb-0">Category: —</h4>
                        </div>
                    </div>

                    <div class="mt-3 p-3 bg-light rounded">
                        <h6 class="fw-bold mb-2">WHO BMI Categories:</h6>
                        <ul class="list-unstyled mb-0 small text-secondary">
                            <li><span class="badge badge-underweight me-2">Underweight</span> &lt; 18.5</li>
                            <li><span class="badge badge-normal me-2">Normal</span> 18.5 – 24.9</li>
                            <li><span class="badge badge-overweight me-2">Overweight</span> 25.0 – 29.9</li>
                            <li><span class="badge badge-obese me-2">Obese</span> ≥ 30.0</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- History & Trend Section -->
        <div class="row g-4 mt-2">
            <div class="col-12">
                <div class="card card-custom p-4 bg-white">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="fw-bold text-secondary mb-0">BMI History & Trend Chart</h4>
                        <div class="d-flex gap-2">
                            <select id="userFilter" class="form-select form-select-sm" style="width: 180px;">
                                <option value="All Users">All Users</option>
                            </select>
                            <button id="btnRefresh" class="btn btn-sm btn-outline-primary">Refresh History</button>
                        </div>
                    </div>

                    <!-- Tabs for Table & Chart -->
                    <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active fw-bold" id="table-tab" data-bs-toggle="tab" data-bs-target="#table-pane" type="button">📋 History Records</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link fw-bold" id="chart-tab" data-bs-toggle="tab" data-bs-target="#chart-pane" type="button">📈 Trend Visualization Graph</button>
                        </li>
                    </ul>

                    <div class="tab-content" id="myTabContent">
                        <div class="tab-pane fade show active" id="table-pane" role="tabpanel">
                            <div class="table-responsive">
                                <table class="table table-hover align-middle">
                                    <thead class="table-light">
                                        <tr>
                                            <th>ID</th>
                                            <th>Date / Time</th>
                                            <th>User Name</th>
                                            <th>Weight (kg)</th>
                                            <th>Height (m)</th>
                                            <th>BMI</th>
                                            <th>Category</th>
                                        </tr>
                                    </thead>
                                    <tbody id="historyBody">
                                        <tr><td colspan="7" class="text-center text-muted">No records loaded.</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="tab-pane fade text-center" id="chart-pane" role="tabpanel">
                            <img id="chartImg" src="/chart?user=All Users" class="img-fluid rounded border shadow-sm" alt="BMI Trend Chart" style="max-height: 450px;">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const form = document.getElementById('bmiForm');
        const alertBox = document.getElementById('alertBox');
        const userFilter = document.getElementById('userFilter');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            alertBox.classList.add('d-none');

            const name = document.getElementById('userName').value;
            const weight = document.getElementById('weight').value;
            const height = document.getElementById('height').value;

            const res = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: name, weight: weight, height: height })
            });

            const data = await res.json();
            if (!data.success) {
                alertBox.textContent = data.message;
                alertBox.classList.remove('d-none');
                return;
            }

            // Display Result
            document.getElementById('resUser').textContent = 'User: ' + data.user_name;
            document.getElementById('resBmi').textContent = 'BMI: ' + data.bmi.toFixed(2);
            document.getElementById('resCategory').textContent = 'Category: ' + data.category;

            const resBox = document.getElementById('resultBox');
            resBox.className = 'result-box ' + data.badge_class;

            loadHistory();
        });

        document.getElementById('btnClear').addEventListener('click', () => {
            form.reset();
            alertBox.classList.add('d-none');
            document.getElementById('resUser').textContent = 'User: —';
            document.getElementById('resBmi').textContent = 'BMI: --.--';
            document.getElementById('resCategory').textContent = 'Category: —';
            document.getElementById('resultBox').className = 'result-box bg-light text-muted';
        });

        async function loadUsers() {
            const res = await fetch('/api/users');
            const data = await res.json();
            const currentVal = userFilter.value;
            userFilter.innerHTML = '<option value="All Users">All Users</option>';
            data.users.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u;
                opt.textContent = u;
                userFilter.appendChild(opt);
            });
            if (data.users.includes(currentVal)) {
                userFilter.value = currentVal;
            }
        }

        async function loadHistory() {
            await loadUsers();
            const selectedUser = userFilter.value;
            const res = await fetch('/api/history?user=' + encodeURIComponent(selectedUser));
            const data = await res.json();

            const tbody = document.getElementById('historyBody');
            tbody.innerHTML = '';

            if (data.records.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No records found.</td></tr>';
            } else {
                data.records.forEach(r => {
                    let badgeClass = 'bg-secondary';
                    if (r.category === 'Underweight') badgeClass = 'badge-underweight';
                    if (r.category === 'Normal') badgeClass = 'badge-normal';
                    if (r.category === 'Overweight') badgeClass = 'badge-overweight';
                    if (r.category === 'Obese') badgeClass = 'badge-obese';

                    const dateStr = (r.created_at || '').substring(0, 16);
                    tbody.innerHTML += `
                        <tr>
                            <td>${r.id}</td>
                            <td>${dateStr}</td>
                            <td class="fw-semibold">${r.user_name}</td>
                            <td>${r.weight.toFixed(1)}</td>
                            <td>${r.height.toFixed(2)}</td>
                            <td class="fw-bold">${r.bmi.toFixed(2)}</td>
                            <td><span class="badge ${badgeClass}">${r.category}</span></td>
                        </tr>
                    `;
                });
            }

            // Update Chart Image
            document.getElementById('chartImg').src = '/chart?user=' + encodeURIComponent(selectedUser) + '&t=' + new Date().getTime();
        }

        userFilter.addEventListener('change', loadHistory);
        document.getElementById('btnRefresh').addEventListener('click', loadHistory);

        // Initial Load
        loadHistory();
    </script>
</body>
</html>
"""

def generate_chart_png(user_name: str) -> bytes:
    """Generates a Matplotlib plot PNG for the web app."""
    if user_name == "All Users":
        success, users = database.get_unique_users()
        user_name = users[0] if (success and users) else "All Users"

    success, records = database.get_user_records(user_name)
    
    fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
    fig.patch.set_facecolor('#F7FAFC')
    ax.set_facecolor('#FFFFFF')

    if not success or not records:
        ax.text(0.5, 0.5, f"No records found for '{user_name}'.\nSave BMI records to display trend chart.",
                horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='#718096', transform=ax.transAxes)
        ax.set_axis_off()
    else:
        dates = [str(r.get('created_at', ''))[:16] for r in records]
        bmis = [r.get('bmi', 0.0) for r in records]

        if len(records) == 1:
            ax.plot(dates, bmis, marker='o', color='#3182CE', markersize=8, linewidth=2)
            ax.set_title(f"BMI Trend — {user_name} (1 Record)", fontsize=13, fontweight='bold', pad=12)
        else:
            ax.plot(dates, bmis, marker='o', color='#2B6CB0', linewidth=2.5, markersize=6)
            ax.set_title(f"BMI Trend Over Time — {user_name}", fontsize=13, fontweight='bold', pad=12)

        ax.axhline(18.5, color='#3182CE', linestyle='--', alpha=0.6, label='Underweight (<18.5)')
        ax.axhline(25.0, color='#DD6B20', linestyle='--', alpha=0.6, label='Overweight (>=25.0)')
        ax.axhline(30.0, color='#E53E3E', linestyle='--', alpha=0.6, label='Obese (>=30.0)')

        ax.set_xlabel("Date & Time", fontsize=10, fontweight='bold')
        ax.set_ylabel("BMI (kg/m²)", fontsize=10, fontweight='bold')
        ax.tick_params(axis='x', rotation=30, labelsize=8)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend(loc='upper left', fontsize=8)

    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


class BMIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress noisy request logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif path == "/chart":
            user_name = query.get("user", ["All Users"])[0]
            img_bytes = generate_chart_png(user_name)
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            self.wfile.write(img_bytes)

        elif path == "/api/users":
            success, users = database.get_unique_users()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "users": users if success else []}).encode("utf-8"))

        elif path == "/api/history":
            selected_user = query.get("user", ["All Users"])[0]
            if selected_user == "All Users":
                success, records = database.get_all_records()
            else:
                success, records = database.get_user_records(selected_user)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "records": records if success else []}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/calculate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            name = data.get("user_name", "")
            weight_str = data.get("weight", "")
            height_str = data.get("height", "")

            is_valid, result = bmi_logic.validate_inputs(name, weight_str, height_str)
            if not is_valid:
                self._send_json({"success": False, "message": result})
                return

            user_name, weight, height = result
            bmi_val = bmi_logic.calculate_bmi(weight, height)
            category, _, _ = bmi_logic.classify_bmi(bmi_val)

            # Save to Database
            database.save_record(user_name, weight, height, bmi_val, category)

            badge_class = "badge-normal"
            if category == "Underweight": badge_class = "badge-underweight"
            if category == "Overweight": badge_class = "badge-overweight"
            if category == "Obese": badge_class = "badge-obese"

            self._send_json({
                "success": True,
                "user_name": user_name,
                "weight": weight,
                "height": height,
                "bmi": bmi_val,
                "category": category,
                "badge_class": badge_class
            })

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main():
    url = f"http://localhost:{PORT}"
    print(f"==================================================")
    print(f"  Smart BMI Calculator — Web Edition")
    print(f"  Server Running on: {url}")
    print(f"  Opening Browser automatically...")
    print(f"==================================================")
    sys.stdout.flush()

    try:
        webbrowser.open(url)
    except Exception:
        pass

    server = HTTPServer((HOST, PORT), BMIRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down web server.")

if __name__ == "__main__":
    main()
