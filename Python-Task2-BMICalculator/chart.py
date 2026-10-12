"""
Chart Module for Smart BMI Calculator
Generates Matplotlib trend visualization charts for user BMI records.
"""

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import List, Dict, Any, Optional

def render_bmi_chart(parent_frame: tk.Widget, user_name: str, records: List[Dict[str, Any]]):
    """
    Renders a Matplotlib BMI trend chart into parent_frame.

    Args:
        parent_frame: Tkinter Frame or Toplevel widget to hold the canvas.
        user_name: Selected user's name.
        records: List of record dictionaries containing 'created_at' and 'bmi'.
    """
    # Clear existing widgets in parent_frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Handle 0 records case
    if not records:
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.text(0.5, 0.5, f"No records found for '{user_name}'.\nSave BMI records to view progress trend.",
                horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='#718096', transform=ax.transAxes)
        ax.set_axis_off()
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return

    # Extract dates and BMI values
    # Format dates nicely (e.g., 'YYYY-MM-DD HH:MM' or short string)
    dates = []
    bmi_values = []
    for r in records:
        raw_date = str(r.get('created_at', ''))
        # Shorten timestamp if full format
        short_date = raw_date[:16] if len(raw_date) >= 16 else raw_date
        dates.append(short_date)
        bmi_values.append(r.get('bmi', 0.0))

    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=100)
    fig.patch.set_facecolor('#F7FAFC')
    ax.set_facecolor('#FFFFFF')

    # Handle 1 record case
    if len(records) == 1:
        ax.plot(dates, bmi_values, marker='o', color='#3182CE', markersize=8, linewidth=2, label='BMI Entry')
        ax.set_title(f"BMI Trend — {user_name} (1 Record)", fontsize=13, fontweight='bold', pad=12)
        ax.text(0.5, 0.15, "Only 1 record available.\nAdd more records over time to display a trend line.",
                horizontalalignment='center', verticalalignment='center',
                fontsize=10, color='#4A5568', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#EBF8FF", edgecolor="#BEE3F8"))
    else:
        # Multiple records plot
        ax.plot(dates, bmi_values, marker='o', color='#2B6CB0', linewidth=2.5, markersize=6, label='BMI')
        ax.set_title(f"BMI Trend Over Time — {user_name}", fontsize=13, fontweight='bold', pad=12)

    # Reference lines for categories
    ax.axhline(18.5, color='#3182CE', linestyle='--', alpha=0.6, label='Underweight (<18.5)')
    ax.axhline(25.0, color='#DD6B20', linestyle='--', alpha=0.6, label='Overweight (>=25.0)')
    ax.axhline(30.0, color='#E53E3E', linestyle='--', alpha=0.6, label='Obese (>=30.0)')

    ax.set_xlabel("Date & Time", fontsize=10, fontweight='bold', labelpad=8)
    ax.set_ylabel("BMI Value (kg/m²)", fontsize=10, fontweight='bold', labelpad=8)
    ax.tick_params(axis='x', rotation=30, labelsize=8)
    ax.tick_params(axis='y', labelsize=9)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper left', fontsize=8, framealpha=0.9)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
