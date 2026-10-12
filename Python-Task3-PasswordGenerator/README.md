# 🔐 Random Password Generator — OASIS INFOBYTE SIP

## OASIS INFOBYTE SIP Internship

* **Track:** Python Programming
* **Task:** Task 3 — Random Password Generator
* **Project Name:** Advanced Password Generator
* **Target Path:** `OIBSIP/Python-Task3-PasswordGenerator/`
* **Intern Name:** Faizan Sayyed
* **Live Demo:** [https://faizan1998sayyed.github.io/OIBSIP/Python-Task3-PasswordGenerator/](https://faizan1998sayyed.github.io/OIBSIP/Python-Task3-PasswordGenerator/)

---

A complete, submission-ready Python **Random Password Generator** application supporting **Beginner CLI**, **Advanced Tkinter GUI**, and **Web Browser** modes.

Built to conform strictly to security standards using Python's built-in **`secrets` module (CS PRNG)** rather than standard pseudo-random number generators.

---

## ✨ Features Checklist

### Beginner Tier (CLI)
- [x] **Length Specification:** Custom password length with minimum 8 characters enforced.
- [x] **Character Types Selection:** Choose Uppercase ($A-Z$), Lowercase ($a-z$), Numbers ($0-9$), and Symbols ($!@\#\$$...). Enforces at least 2 types selected.
- [x] **Criteria Matching:** Generates passwords matching all user criteria.
- [x] **Input Validation:** Rejects lengths $<8$ or $<2$ character types selected.
- [x] **Continuous Generation:** Option to generate multiple passwords without restarting.

### Advanced Tier (Tkinter GUI & Web Browser)
- [x] **Interactive GUI:** Tkinter GUI with length slider ($8 - 64$), spinbox, and checkboxes.
- [x] **Cryptographically Secure PRNG:** Built using `secrets` module (`secrets.choice` & `secrets.SystemRandom().shuffle`).
- [x] **Password Strength Indicator:** Real-time visual progress bar and label based on Shannon Bit Entropy ($E = L \times \log_2(N)$):
  - 🔴 **Weak** ($E < 40$ bits or length $< 10$)
  - 🟠 **Medium** ($40 \le E < 60$ bits)
  - 🟢 **Strong** ($60 \le E < 80$ bits)
  - 🔵 **Very Strong / Bulletproof** ($E \ge 80$ bits)
- [x] **Security Rules Enforced:** Guaranteed to contain at least **1 character from EACH selected type**.
- [x] **Clipboard Integration:** "Copy to Clipboard" button (`pyperclip` with automatic fallback to `tkinter.clipboard`). Auto-copies on generation.
- [x] **Ambiguous Character Filtering:** Option to exclude visually confusing characters (`0, O, o, 1, l, I, |`).
- [x] **Session History:** Keeps an in-memory list of the last 5 generated passwords in the current session (**zero disk persistence** for maximum security).
- [x] **Web Browser Edition:** Run the generator directly inside your Web Browser at `http://localhost:5000` via `python web_app.py`.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.12+
- **Security Engine:** `secrets` (Python Standard Library CS PRNG)
- **GUI Framework:** `tkinter` & `ttk`
- **Clipboard Utility:** `pyperclip` (Optional, auto-fallback built-in)
- **Web Interface:** Python `http.server` + Bootstrap 5 HTML/CSS/JS

---

## 💻 Installation & Setup

1. Open PowerShell or Command Prompt in the project folder:
   ```cmd
   cd D:\Practice\password_generates
   ```

2. Install optional third-party packages:
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
*Opens `http://localhost:5000` automatically in your web browser!*

---

## 🧪 Running Automated Unit Tests

To run the automated security and logic test suite:

```cmd
python test_runner.py
```

Expected Output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.005s

OK
```

---

## 📁 Project Structure

```
Python-Task3-PasswordGenerator/
├── generator_logic.py         # Pure secrets CS PRNG, diversity rules & entropy strength evaluation
├── cli_app.py                 # Beginner Tier: Interactive CLI interface
├── gui_app.py                 # Advanced Tier: Tkinter GUI with sliders, strength bar, clipboard & history
├── main.py                    # Main launcher entry point (Tkinter GUI by default, --cli flag support)
├── web_app.py                 # Browser Launcher (Bootstrap 5 Web Interface)
├── test_runner.py             # Automated unit test suite (5/5 passing)
├── requirements.txt           # Dependencies (pyperclip)
├── README.md                  # Complete documentation
└── .gitignore                 # Standard Python gitignore
```
