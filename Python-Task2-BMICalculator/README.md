# Smart BMI Calculator — OASIS INFOBYTE SIP

## OASIS INFOBYTE SIP Internship

* **Track:** Python Programming
* **Task:** Task 2 — BMI Calculator
* **Project Name:** Smart BMI Calculator
* **Target Path:** `OIBSIP/Python-Task2-BMICalculator/`

---

## 📌 Project Objective

The **Smart BMI Calculator** is a full-featured, professional Python desktop application built for calculating, tracking, and visualizing Body Mass Index (BMI). It features a modern Tkinter Graphical User Interface, multi-user support, persistent SQLite storage, color-coded classification feedback, and Matplotlib chronological trend analysis.

This application is submission-ready, easy to demonstrate in screen-recorded videos, and built cleanly following modular Python design principles.

---

## 🌟 Key Features

* **Instant BMI Calculation:** Computes BMI accurately based on standard height ($m$) and weight ($kg$).
* **Exact Classification:** Categorizes BMI according to WHO standards with boundary precision.
* **Color-Coded Visual Results:** Displays visual status indicators (Blue = Underweight, Green = Normal, Orange = Overweight, Red = Obese).
* **Robust Input Validation:** Catches empty inputs, non-numeric strings, zero height, and negative values with clear GUI warning dialogs.
* **Multi-User History:** Tracks records for multiple users (e.g. Faizan, Ahmed, Rahul) without overwriting existing data.
* **SQLite Persistence:** Automatically creates `bmi_records.db` on launch and saves records permanently.
* **Matplotlib Trend Graph:** Renders line charts of BMI progress over time for individual users, complete with threshold markers.
* **Built-in Demo Title Card:** Includes a 2-second static title card launcher for screen recording videos.
* **Error Handling:** Safe database connection and query handling with parameterized SQL statements.

---

## 🛠️ Technologies Used

* **Python 3.12+**
* **Tkinter & ttk** (Standard Python GUI library)
* **SQLite3** (Built-in Relational Database)
* **Matplotlib** (Data visualization & trend plotting)

---

## 📐 BMI Formula & Standard Categories

### Formula
$$\text{BMI} = \frac{\text{Weight (kg)}}{\text{Height (m)}^2}$$

The calculated BMI is displayed rounded to **exactly 2 decimal places**.

### Categories

| Category | BMI Range | Visual Feedback Color |
| :--- | :--- | :--- |
| **Underweight** | $< 18.5$ | Informational Blue (`#3182CE`) |
| **Normal** | $18.5 - 24.9$ | Green (`#38A169`) |
| **Overweight** | $25.0 - 29.9$ | Warning Orange (`#DD6B20`) |
| **Obese** | $\ge 30.0$ | Red (`#E53E3E`) |

---

## 📁 Project Structure

```
OIBSIP/
└── Python-Task2-BMICalculator/
    ├── main.py                    # Main Tkinter GUI application & event handlers
    ├── bmi_logic.py              # Pure calculation, category classification & input validation logic
    ├── database.py               # SQLite connection, schema creation & parameterized CRUD operations
    ├── chart.py                  # Matplotlib trend line chart renderer for Tkinter
    ├── test_runner.py            # Automated unit test suite
    ├── requirements.txt          # Third-party package dependencies (matplotlib)
    ├── .gitignore                # Excludes bytecode, venv, and local SQLite DB
    ├── README.md                 # Complete project documentation & guide
    ├── DEMO_SCRIPT.md            # Video recording sequence & timing script
    ├── LINKEDIN_POST.md          # Professional LinkedIn submission post draft
    ├── PEER_EVALUATION_GUIDE.md  # Substantive peer review comment examples
    └── SUBMISSION_CHECKLIST.md   # Final task compliance checklist
```

---

## 💻 Installation & Setup (Windows)

1. Open PowerShell / Command Prompt and navigate to the project folder:
   ```cmd
   cd OIBSIP\Python-Task2-BMICalculator
   ```

2. Create a virtual environment (recommended):
   ```cmd
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

4. Install third-party requirements:
   ```cmd
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Application

Launch the GUI application directly with Python:

```cmd
python main.py
```

No command-line interaction is required once launched.

---

## 🧪 Running Automated Tests

To run the unit tests for calculation logic, boundary classifications, input validation, and SQLite database storage:

```cmd
python test_runner.py
```

Expected output:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.124s

OK
```

---

## 🗄️ Database Architecture

The application uses an embedded **SQLite3** database (`bmi_records.db`), which is automatically created upon first launch.

### Table Schema: `bmi_records`
```sql
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

* All SQL queries use **parameterized placeholders (`?`)** to prevent SQL injection.
* DB errors are safely caught and displayed using `tkinter.messagebox.showerror`.

---

## 📷 Application Screenshots (Placeholders)

* **Main Calculator View:** Shows user inputs, Calculate button, and color-coded result badge.
* **BMI History View:** Displays Treeview table populated with records filtered by user.
* **BMI Trend Graph:** Displays Matplotlib progress chart with threshold reference lines.
* **Input Validation Alert:** Shows warning dialog when invalid height/weight is entered.
* **Demo Title Card:** Static 2-second title card for video recording.

---

## 🎥 Demo Video Guide

The application includes a built-in **"🎬 Demo Title Card (2s)"** button at the top right of the window.

### Recording Sequence:
1. Click **Demo Title Card** (shows Name, Track, Task for 2 seconds).
2. Enter User Name (e.g., `Faizan`), Weight (`70`), Height (`1.75`).
3. Click **CALCULATE BMI** -> Show `BMI: 22.86` and `Category: Normal` (Green).
4. Click **SAVE RECORD**.
5. Add a second record for `Faizan` (`68 kg`, `1.75 m` -> `BMI: 22.20`). Save record.
6. Switch to **History & Trends** tab. Select `Faizan` in user dropdown.
7. Click **Show Trend Chart** -> View Matplotlib line chart.
8. Demonstrate input validation (e.g. clear fields and click Calculate to show warning box).
