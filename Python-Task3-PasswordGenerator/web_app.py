"""
Smart Web Browser Launcher for Random Password Generator
Runs a local web server and opens the application in your default Web Browser.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os
import sys
import webbrowser
import generator_logic

PORT = 5001
HOST = "0.0.0.0"

# In-memory history for web session
SESSION_HISTORY = []

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Cryptographically Secure Password Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f7fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-custom { border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: none; }
        .pwd-box { font-family: 'Consolas', monospace; font-size: 1.4rem; letter-spacing: 1px; font-weight: bold; background: #edf2f7; text-align: center; }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 800px;">
        <div class="d-flex justify-content-between align-items-center mb-4 bg-white p-3 rounded shadow-sm">
            <div>
                <h3 class="fw-bold mb-0 text-primary">🔐 RANDOM PASSWORD GENERATOR</h3>
                <small class="text-muted">Python CS PRNG (secrets module) • Browser Edition</small>
            </div>
            <span class="badge bg-success fs-6">🌐 Browser Edition Active</span>
        </div>

        <!-- Generated Password Result Panel -->
        <div class="card card-custom p-4 bg-white mb-4">
            <h5 class="fw-bold text-secondary mb-3">Generated Password</h5>
            <div class="input-group input-group-lg mb-3">
                <input type="text" id="pwdOutput" class="form-control pwd-box" readonly placeholder="Click Generate below...">
                <button class="btn btn-success fw-bold px-4" id="btnCopy">📋 Copy</button>
            </div>

            <div class="d-flex justify-content-between align-items-center mb-1">
                <span id="lblStrength" class="fw-bold text-muted">Strength: —</span>
                <span id="lblEntropy" class="text-secondary small">Entropy: 0.0 bits</span>
            </div>
            <div class="progress" style="height: 12px;">
                <div id="progBar" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%;"></div>
            </div>
        </div>

        <!-- Criteria & Controls -->
        <div class="card card-custom p-4 bg-white mb-4">
            <h5 class="fw-bold text-secondary mb-3">Password Controls & Criteria</h5>
            <form id="genForm">
                <div class="mb-4">
                    <div class="d-flex justify-content-between">
                        <label class="form-label fw-bold">Password Length (min 8):</label>
                        <span id="lenVal" class="fw-bold text-primary fs-5">16</span>
                    </div>
                    <input type="range" class="form-range" id="lengthRange" min="8" max="64" value="16">
                </div>

                <div class="row g-3 mb-4">
                    <div class="col-md-6">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="chkUpper" checked>
                            <label class="form-check-label fw-semibold" for="chkUpper">Uppercase Letters (A-Z)</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="chkLower" checked>
                            <label class="form-check-label fw-semibold" for="chkLower">Lowercase Letters (a-z)</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="chkDigits" checked>
                            <label class="form-check-label fw-semibold" for="chkDigits">Numbers (0-9)</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="chkSymbols" checked>
                            <label class="form-check-label fw-semibold" for="chkSymbols">Symbols (!@#$...)</label>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="chkAmbiguous">
                            <label class="form-check-label text-danger fw-semibold" for="chkAmbiguous">Exclude Ambiguous Characters (0, O, o, 1, l, I, |)</label>
                        </div>
                    </div>
                </div>

                <div class="d-grid">
                    <button type="submit" class="btn btn-primary btn-lg fw-bold">⚡ GENERATE NEW PASSWORD</button>
                </div>
            </form>
        </div>

        <!-- Session History -->
        <div class="card card-custom p-4 bg-white">
            <h5 class="fw-bold text-secondary mb-3">Session History (Last 5 Passwords — Memory Only)</h5>
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Generated Password</th>
                            <th class="text-center">Length</th>
                            <th class="text-center">Strength</th>
                            <th class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody id="historyBody">
                        <tr><td colspan="4" class="text-center text-muted">No passwords generated yet.</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Copy Alert Toast -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="copyToast" class="toast align-items-center text-bg-success border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body fw-bold">
                    📋 Password copied to clipboard!
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const lengthRange = document.getElementById('lengthRange');
        const lenVal = document.getElementById('lenVal');
        const pwdOutput = document.getElementById('pwdOutput');
        const btnCopy = document.getElementById('btnCopy');
        const toastEl = document.getElementById('copyToast');
        const toast = new bootstrap.Toast(toastEl);

        lengthRange.addEventListener('input', () => {
            lenVal.textContent = lengthRange.value;
        });

        async function generatePassword() {
            const length = parseInt(lengthRange.value);
            const use_upper = document.getElementById('chkUpper').checked;
            const use_lower = document.getElementById('chkLower').checked;
            const use_digits = document.getElementById('chkDigits').checked;
            const use_symbols = document.getElementById('chkSymbols').checked;
            const exclude_ambiguous = document.getElementById('chkAmbiguous').checked;

            const res = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
                })
            });

            const data = await res.json();
            if (!data.success) {
                alert(data.message);
                return;
            }

            pwdOutput.value = data.password;

            // Update Strength UI
            document.getElementById('lblStrength').textContent = 'Strength: ' + data.strength.label;
            document.getElementById('lblEntropy').textContent = 'Entropy: ' + data.strength.entropy + ' bits';

            const bar = document.getElementById('progBar');
            bar.style.width = data.strength.score + '%';
            bar.style.backgroundColor = data.strength.color;

            // Copy automatically
            navigator.clipboard.writeText(data.password);
            toast.show();

            loadHistory();
        }

        document.getElementById('genForm').addEventListener('submit', (e) => {
            e.preventDefault();
            generatePassword();
        });

        btnCopy.addEventListener('click', () => {
            if (pwdOutput.value) {
                navigator.clipboard.writeText(pwdOutput.value);
                toast.show();
            }
        });

        async function loadHistory() {
            const res = await fetch('/api/history');
            const data = await res.json();
            const tbody = document.getElementById('historyBody');
            tbody.innerHTML = '';

            if (data.history.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No passwords generated yet.</td></tr>';
            } else {
                data.history.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td class="fw-bold text-break">${item.password}</td>
                        <td class="text-center">${item.length}</td>
                        <td class="text-center"><span class="badge bg-secondary">${item.strength}</span></td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-outline-primary fw-bold" onclick="copyText('${item.password}')">Copy</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }
        }

        function copyText(txt) {
            navigator.clipboard.writeText(txt);
            pwdOutput.value = txt;
            toast.show();
        }

        // Initial Generation on page load
        generatePassword();
    </script>
</body>
</html>
"""

class PasswordRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress server logs

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif self.path == "/api/history":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"history": SESSION_HISTORY}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            length = int(data.get("length", 16))
            use_upper = bool(data.get("use_upper", True))
            use_lower = bool(data.get("use_lower", True))
            use_digits = bool(data.get("use_digits", True))
            use_symbols = bool(data.get("use_symbols", True))
            exclude_ambiguous = bool(data.get("exclude_ambiguous", False))

            success, pwd_or_err = generator_logic.generate_password(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous
            )

            if not success:
                self._send_json({"success": False, "message": pwd_or_err})
                return

            strength = generator_logic.calculate_strength(
                pwd_or_err, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
            )

            # Store in session history
            SESSION_HISTORY.insert(0, {
                "password": pwd_or_err,
                "length": len(pwd_or_err),
                "strength": strength['label']
            })
            if len(SESSION_HISTORY) > 5:
                SESSION_HISTORY.pop()

            self._send_json({
                "success": True,
                "password": pwd_or_err,
                "strength": strength
            })

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main():
    url = f"http://localhost:{PORT}"
    print("==================================================")
    print("  Random Password Generator — Web Edition")
    print(f"  Server Running on: {url}")
    print("  Opening Browser automatically...")
    print("==================================================")
    sys.stdout.flush()

    try:
        webbrowser.open(url)
    except Exception:
        pass

    server = HTTPServer((HOST, PORT), PasswordRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down web server.")

if __name__ == "__main__":
    main()
