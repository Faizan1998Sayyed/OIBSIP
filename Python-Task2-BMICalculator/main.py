"""
Smart BMI Calculator — Main GUI Application
OASIS INFOBYTE SIP — Task 2: BMI Calculator
Track: Python Programming
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Import custom modules
import bmi_logic
import database
import chart

class BMICalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart BMI Calculator")
        self.root.geometry("950x700")
        self.root.minsize(850, 600)

        # Apply clean theme/style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()

        # Initialize SQLite Database
        success, db_msg = database.init_db()
        if not success:
            messagebox.showerror("Database Error", f"Failed to initialize database:\n{db_msg}")

        # Current calculation result cache
        self.last_calculated = None

        # Build GUI Layout
        self._build_ui()
        self._refresh_user_dropdowns()
        self.refresh_history_table()

    def _configure_styles(self):
        """Configure custom styles for buttons, labels, and entry fields."""
        bg_color = "#F7FAFC"
        self.root.configure(bg=bg_color)

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=bg_color, foreground="#2D3748")

        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1A202C", background=bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#718096", background=bg_color)
        self.style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"), foreground="#4A5568", background=bg_color)

        # Buttons
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#3182CE", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#2B6CB0")])

        self.style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background="#38A169", foreground="#FFFFFF")
        self.style.map("Success.TButton", background=[("active", "#2F855A")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 10), background="#E2E8F0", foreground="#2D3748")
        self.style.map("Secondary.TButton", background=[("active", "#CBD5E0")])

        self.style.configure("TitleCard.TButton", font=("Segoe UI", 9, "bold"), background="#805AD5", foreground="#FFFFFF")
        self.style.map("TitleCard.TButton", background=[("active", "#6B46C1")])

    def _build_ui(self):
        """Construct main window widgets."""
        # Top Header Frame
        header_frame = ttk.Frame(self.root, padding="15 15 15 10")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(header_frame, text="SMART BMI CALCULATOR", style="Header.TLabel")
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(header_frame, text="OASIS INFOBYTE SIP — Task 2", style="SubHeader.TLabel")
        subtitle_label.pack(side=tk.LEFT, padx=15, pady=(6, 0))

        # Title Card Button for Demo Video
        btn_title_card = ttk.Button(header_frame, text="🎬 Demo Title Card (2s)", style="TitleCard.TButton", command=self.show_title_card)
        btn_title_card.pack(side=tk.RIGHT)

        # Main Notebook Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Tab 1: Calculator
        self.calc_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.calc_tab, text="  BMI Calculator  ")

        # Tab 2: History & Trend
        self.history_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.history_tab, text="  History & Trends  ")

        self._build_calculator_tab()
        self._build_history_tab()

    def _build_calculator_tab(self):
        """Build elements inside Calculator Tab."""
        # Left Side: Inputs & Actions
        input_frame = ttk.LabelFrame(self.calc_tab, text=" User Input Details ", padding="20")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # User Name
        ttk.Label(input_frame, text="User Name:", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.entry_name = ttk.Entry(input_frame, font=("Segoe UI", 11), width=25)
        self.entry_name.grid(row=0, column=1, sticky=tk.EW, pady=8, padx=10)
        self.entry_name.focus()

        # Weight
        ttk.Label(input_frame, text="Weight (kg):", style="Field.TLabel").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.entry_weight = ttk.Entry(input_frame, font=("Segoe UI", 11), width=25)
        self.entry_weight.grid(row=1, column=1, sticky=tk.EW, pady=8, padx=10)

        # Height
        ttk.Label(input_frame, text="Height (m):", style="Field.TLabel").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.entry_height = ttk.Entry(input_frame, font=("Segoe UI", 11), width=25)
        self.entry_height.grid(row=2, column=1, sticky=tk.EW, pady=8, padx=10)

        # Buttons Frame
        btn_frame = ttk.Frame(input_frame, padding="0 15 0 0")
        btn_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW)

        btn_calc = ttk.Button(btn_frame, text="CALCULATE BMI", style="Primary.TButton", command=self.on_calculate)
        btn_calc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_save = ttk.Button(btn_frame, text="SAVE RECORD", style="Success.TButton", command=self.on_save_record)
        btn_save.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_clear = ttk.Button(btn_frame, text="CLEAR FIELDS", style="Secondary.TButton", command=self.on_clear_fields)
        btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Quick navigation buttons
        nav_frame = ttk.Frame(input_frame, padding="0 15 0 0")
        nav_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)

        btn_view_hist = ttk.Button(nav_frame, text="View History", style="Secondary.TButton", command=lambda: self.notebook.select(self.history_tab))
        btn_view_hist.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_view_trend = ttk.Button(nav_frame, text="Show BMI Trend Graph", style="Secondary.TButton", command=self.on_show_trend_tab)
        btn_view_trend.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Right Side: Color-coded Result Display Panel
        self.result_frame = ttk.LabelFrame(self.calc_tab, text=" BMI Result ", padding="20")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.lbl_result_user = ttk.Label(self.result_frame, text="User: —", font=("Segoe UI", 12))
        self.lbl_result_user.pack(anchor=tk.W, pady=(5, 10))

        self.lbl_result_bmi = tk.Label(self.result_frame, text="BMI: --.--", font=("Segoe UI", 26, "bold"), fg="#718096", bg="#EDF2F7", pady=15)
        self.lbl_result_bmi.pack(fill=tk.X, pady=10)

        self.lbl_result_category = tk.Label(self.result_frame, text="Category: —", font=("Segoe UI", 14, "bold"), fg="#4A5568", bg="#EDF2F7", pady=10)
        self.lbl_result_category.pack(fill=tk.X, pady=(0, 10))

        # Category Reference Chart
        ref_frame = ttk.Frame(self.result_frame)
        ref_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Label(ref_frame, text="Reference Standard:", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(ref_frame, text="• Underweight: < 18.5\n• Normal: 18.5 – 24.9\n• Overweight: 25.0 – 29.9\n• Obese: ≥ 30.0",
                  font=("Segoe UI", 9), foreground="#718096").pack(anchor=tk.W, padx=5)

    def _build_history_tab(self):
        """Build elements inside History & Trends Tab."""
        top_bar = ttk.Frame(self.history_tab, padding="0 0 0 10")
        top_bar.pack(fill=tk.X)

        ttk.Label(top_bar, text="Select User:", style="Field.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.combo_user_filter = ttk.Combobox(top_bar, state="readonly", font=("Segoe UI", 10), width=20)
        self.combo_user_filter.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_user_filter.bind("<<ComboboxSelected>>", self.on_user_filter_changed)

        btn_refresh = ttk.Button(top_bar, text="Refresh Data", style="Secondary.TButton", command=self.refresh_history_table)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        btn_show_graph = ttk.Button(top_bar, text="📈 Show Trend Chart", style="Primary.TButton", command=self.on_render_selected_trend)
        btn_show_graph.pack(side=tk.LEFT, padx=5)

        # Split PanedWindow: Top History Table, Bottom Trend Chart
        paned = ttk.PanedWindow(self.history_tab, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Treeview History Table Container
        tree_frame = ttk.Frame(paned)
        paned.add(tree_frame, weight=1)

        columns = ("id", "datetime", "user", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

        self.tree.heading("id", text="ID")
        self.tree.heading("datetime", text="Date / Time")
        self.tree.heading("user", text="User Name")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("height", text="Height (m)")
        self.tree.heading("bmi", text="BMI")
        self.tree.heading("category", text="Category")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("datetime", width=140, anchor=tk.CENTER)
        self.tree.column("user", width=120, anchor=tk.W)
        self.tree.column("weight", width=90, anchor=tk.CENTER)
        self.tree.column("height", width=90, anchor=tk.CENTER)
        self.tree.column("bmi", width=80, anchor=tk.CENTER)
        self.tree.column("category", width=110, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Matplotlib Chart Frame Container
        self.chart_container = ttk.LabelFrame(paned, text=" BMI Progress Trend Visualization ", padding="10")
        paned.add(self.chart_container, weight=1)

    def on_calculate(self):
        """Validate input and display calculation result in GUI."""
        name = self.entry_name.get()
        weight_str = self.entry_weight.get()
        height_str = self.entry_height.get()

        is_valid, result = bmi_logic.validate_inputs(name, weight_str, height_str)
        if not is_valid:
            messagebox.showwarning("Input Validation Warning", result)
            return

        user_name, weight, height = result
        bmi_val = bmi_logic.calculate_bmi(weight, height)
        category, bg_color, fg_color = bmi_logic.classify_bmi(bmi_val)

        # Store in calculation cache
        self.last_calculated = {
            'user_name': user_name,
            'weight': weight,
            'height': height,
            'bmi': bmi_val,
            'category': category
        }

        # Update GUI Display
        self.lbl_result_user.config(text=f"User: {user_name}")
        self.lbl_result_bmi.config(text=f"BMI: {bmi_val:.2f}", bg=bg_color, fg=fg_color)
        self.lbl_result_category.config(text=f"Category: {category}", bg=bg_color, fg=fg_color)

    def on_save_record(self):
        """Saves current record to SQLite database."""
        if not self.last_calculated:
            # If user hasn't clicked calculate yet, try calculating first
            name = self.entry_name.get()
            weight_str = self.entry_weight.get()
            height_str = self.entry_height.get()

            is_valid, result = bmi_logic.validate_inputs(name, weight_str, height_str)
            if not is_valid:
                messagebox.showwarning("Input Validation Warning", result)
                return

            user_name, weight, height = result
            bmi_val = bmi_logic.calculate_bmi(weight, height)
            category, _, _ = bmi_logic.classify_bmi(bmi_val)
            self.last_calculated = {
                'user_name': user_name,
                'weight': weight,
                'height': height,
                'bmi': bmi_val,
                'category': category
            }

        rec = self.last_calculated
        success, db_msg = database.save_record(rec['user_name'], rec['weight'], rec['height'], rec['bmi'], rec['category'])

        if success:
            messagebox.showinfo("Success", f"BMI record for '{rec['user_name']}' saved successfully!")
            self._refresh_user_dropdowns()
            self.refresh_history_table()
        else:
            messagebox.showerror("Database Error", f"Could not save record:\n{db_msg}")

    def on_clear_fields(self):
        """Clears all input entry fields and resets result panel."""
        self.entry_name.delete(0, tk.END)
        self.entry_weight.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)

        self.last_calculated = None
        self.lbl_result_user.config(text="User: —")
        self.lbl_result_bmi.config(text="BMI: --.--", bg="#EDF2F7", fg="#718096")
        self.lbl_result_category.config(text="Category: —", bg="#EDF2F7", fg="#4A5568")
        self.entry_name.focus()

    def _refresh_user_dropdowns(self):
        """Updates user filter dropdown list with unique users from DB."""
        success, users = database.get_unique_users()
        if success:
            options = ["All Users"] + users
            self.combo_user_filter['values'] = options
            if not self.combo_user_filter.get():
                self.combo_user_filter.current(0)

    def refresh_history_table(self):
        """Refreshes Treeview history table based on current user filter."""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_user = self.combo_user_filter.get()
        if not selected_user or selected_user == "All Users":
            success, records = database.get_all_records()
        else:
            success, records = database.get_user_records(selected_user)

        if not success:
            messagebox.showerror("Database Error", f"Failed to retrieve history:\n{records}")
            return

        for r in records:
            created_str = str(r['created_at'])[:16]
            self.tree.insert("", tk.END, values=(
                r['id'],
                created_str,
                r['user_name'],
                f"{r['weight']:.1f}",
                f"{r['height']:.2f}",
                f"{r['bmi']:.2f}",
                r['category']
            ))

    def on_user_filter_changed(self, event=None):
        """Triggered when user dropdown filter changes."""
        self.refresh_history_table()
        self.on_render_selected_trend()

    def on_show_trend_tab(self):
        """Switch to History/Trend tab and display graph for current user."""
        current_name = self.entry_name.get().strip()
        if current_name:
            if current_name in self.combo_user_filter['values']:
                self.combo_user_filter.set(current_name)
        self.notebook.select(self.history_tab)
        self.on_render_selected_trend()

    def on_render_selected_trend(self):
        """Fetches records for selected user and renders Matplotlib chart."""
        selected_user = self.combo_user_filter.get()
        if not selected_user or selected_user == "All Users":
            # If "All Users" is selected, pick the first available individual user or prompt user
            users = [u for u in self.combo_user_filter['values'] if u != "All Users"]
            if users:
                selected_user = users[0]
                self.combo_user_filter.set(selected_user)
            else:
                chart.render_bmi_chart(self.chart_container, "No Users", [])
                return

        success, records = database.get_user_records(selected_user)
        if success:
            chart.render_bmi_chart(self.chart_container, selected_user, records)
        else:
            messagebox.showerror("Database Error", f"Failed to load chart data:\n{records}")

    def show_title_card(self):
        """Displays a static 2-second Title Card window formatted for demo video recording."""
        card_win = tk.Toplevel(self.root)
        card_win.title("OASIS INFOBYTE SIP — Demo Title Card")
        card_win.geometry("600x400")
        card_win.configure(bg="#1A202C")
        card_win.grab_set()

        # Center top card
        frame = tk.Frame(card_win, bg="#1A202C", padx=30, pady=30)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="OASIS INFOBYTE SIP", font=("Segoe UI", 16, "bold"), fg="#CBD5E0", bg="#1A202C").pack(pady=(10, 5))
        tk.Label(frame, text="TASK 2 — BMI CALCULATOR", font=("Segoe UI", 20, "bold"), fg="#63B3ED", bg="#1A202C").pack(pady=(0, 20))

        info_box = tk.Frame(frame, bg="#2D3748", padx=20, pady=20)
        info_box.pack(fill=tk.X, pady=10)

        tk.Label(info_box, text="Full Name: Faizan Sayyed", font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Assigned Track: Python Programming", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Project: Smart BMI Calculator", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)

        timer_lbl = tk.Label(frame, text="Static Title Card (Auto-closes in 2s)...", font=("Segoe UI", 10, "italic"), fg="#A0AEC0", bg="#1A202C")
        timer_lbl.pack(pady=(15, 0))

        # Auto close after 2000 ms (2 seconds)
        card_win.after(2000, card_win.destroy)

def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
