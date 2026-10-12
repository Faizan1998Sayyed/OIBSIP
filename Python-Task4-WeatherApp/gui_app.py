"""
GUI Application for Basic Weather App (Advanced Tier)
Tkinter GUI with city search, auto IP location detection, unit toggle (°C/°F),
hourly forecast (next 6 hours), daily forecast (next 5 days), and visual weather icons.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import weather_service

class WeatherAppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🌤️ Basic Weather App — Advanced Edition")
        self.root.geometry("850x700")
        self.root.minsize(800, 650)
        self.root.configure(bg="#F7FAFC")

        # Current display unit state: "metric" (°C) or "imperial" (°F)
        self.unit = "metric" # "metric" = °C, "imperial" = °F
        self.current_data = None

        # Configure custom styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()

        # Build GUI layout
        self._build_ui()

        # Auto-detect location on app start
        self.root.after(500, self.on_auto_detect_location)

    def _configure_styles(self):
        bg_color = "#F7FAFC"
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=bg_color, foreground="#2D3748")

        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1A202C", background=bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#718096", background=bg_color)
        self.style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"), foreground="#4A5568", background=bg_color)

        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#3182CE", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#2B6CB0")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 9), background="#E2E8F0", foreground="#2D3748")
        self.style.map("Secondary.TButton", background=[("active", "#CBD5E0")])

        self.style.configure("Unit.TButton", font=("Segoe UI", 10, "bold"), background="#805AD5", foreground="#FFFFFF")
        self.style.map("Unit.TButton", background=[("active", "#6B46C1")])

    def _build_ui(self):
        # Top Bar: Search Controls
        top_frame = ttk.Frame(self.root, padding="15 15 15 5")
        top_frame.pack(fill=tk.X)

        title = ttk.Label(top_frame, text="🌤️ BASIC WEATHER APP", style="Header.TLabel")
        title.pack(side=tk.LEFT)

        # Title Card Button for Demo Video (OASIS INFOBYTE requirement)
        btn_title_card = ttk.Button(top_frame, text="🎬 Demo Title Card (2s)", style="Secondary.TButton", command=self.show_title_card)
        btn_title_card.pack(side=tk.RIGHT, padx=(5, 0))

        # Unit Toggle Button
        self.btn_unit = ttk.Button(top_frame, text="Unit: °C / °F", style="Unit.TButton", command=self.toggle_units)
        self.btn_unit.pack(side=tk.RIGHT, padx=5)

        # Auto IP Location Button
        btn_auto = ttk.Button(top_frame, text="📍 Auto Location", style="Secondary.TButton", command=self.on_auto_detect_location)
        btn_auto.pack(side=tk.RIGHT, padx=5)

        # Search Form Bar
        search_frame = ttk.Frame(self.root, padding="15 5 15 10")
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="City / ZIP:", style="Field.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_city = ttk.Entry(search_frame, font=("Segoe UI", 11), width=25)
        self.entry_city.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_city.bind("<Return>", lambda e: self.on_get_weather())
        self.entry_city.focus()

        btn_search = ttk.Button(search_frame, text="GET WEATHER", style="Primary.TButton", command=self.on_get_weather)
        btn_search.pack(side=tk.LEFT)

        # In-GUI Error Alert Banner
        self.lbl_error = tk.Label(self.root, text="", font=("Segoe UI", 10, "bold"), fg="#9B2C2C", bg="#FED7D7", pady=6)
        # Hidden by default

        # Main Scrollable Content Paned Window
        self.main_content = ttk.Frame(self.root, padding="15 5 15 15")
        self.main_content.pack(fill=tk.BOTH, expand=True)

        # Hero Weather Panel
        self.hero_frame = ttk.LabelFrame(self.main_content, text=" Current Weather ", padding="15")
        self.hero_frame.pack(fill=tk.X, pady=(0, 10))

        hero_inner = ttk.Frame(self.hero_frame)
        hero_inner.pack(fill=tk.X)

        # Left Hero: City & Temp
        hero_left = ttk.Frame(hero_inner)
        hero_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_city = ttk.Label(hero_left, text="Search a city above...", font=("Segoe UI", 18, "bold"), foreground="#2B6CB0")
        self.lbl_city.pack(anchor=tk.W)

        self.lbl_temp = ttk.Label(hero_left, text="--°", font=("Segoe UI", 36, "bold"), foreground="#1A202C")
        self.lbl_temp.pack(anchor=tk.W)

        self.lbl_condition = ttk.Label(hero_left, text="Condition: —", font=("Segoe UI", 12, "bold"), foreground="#4A5568")
        self.lbl_condition.pack(anchor=tk.W)

        # Right Hero: Stats (Humidity, Wind, Source)
        hero_right = ttk.Frame(hero_inner)
        hero_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_humidity = ttk.Label(hero_right, text="💧 Humidity: —%", font=("Segoe UI", 11))
        self.lbl_humidity.pack(anchor=tk.E, pady=3)

        self.lbl_wind = ttk.Label(hero_right, text="💨 Wind Speed: —", font=("Segoe UI", 11))
        self.lbl_wind.pack(anchor=tk.E, pady=3)

        self.lbl_source = ttk.Label(hero_right, text="📡 Source: —", font=("Segoe UI", 9, "italic"), foreground="#718096")
        self.lbl_source.pack(anchor=tk.E, pady=3)

        # Hourly Forecast Panel (Next 6 Hours)
        self.hourly_frame = ttk.LabelFrame(self.main_content, text=" 🕒 6-Hour Hourly Forecast ", padding="10")
        self.hourly_frame.pack(fill=tk.X, pady=(0, 10))

        self.hourly_container = ttk.Frame(self.hourly_frame)
        self.hourly_container.pack(fill=tk.X)

        # Daily Forecast Panel (Next 5 Days)
        self.daily_frame = ttk.LabelFrame(self.main_content, text=" 📅 5-Day Daily Forecast ", padding="10")
        self.daily_frame.pack(fill=tk.BOTH, expand=True)

        self.daily_container = ttk.Frame(self.daily_frame)
        self.daily_container.pack(fill=tk.BOTH, expand=True)

    def show_error(self, message: str):
        """Displays error inside GUI banner without crashing."""
        self.lbl_error.config(text=f"⚠️  {message}")
        self.lbl_error.pack(fill=tk.X, padx=15, pady=(0, 10), before=self.main_content)

    def hide_error(self):
        """Hides GUI error banner."""
        self.lbl_error.pack_forget()

    def on_auto_detect_location(self):
        """Auto-detects location via IP address."""
        self.hide_error()
        success, loc_info = weather_service.auto_detect_location()
        if success:
            city_name = loc_info.get("city", "")
            if city_name and city_name != "Unknown":
                self.entry_city.delete(0, tk.END)
                self.entry_city.insert(0, city_name)
                self.on_get_weather()
                return

        self.show_error("Could not auto-detect IP location. Please search for your city manually.")

    def on_get_weather(self):
        """Fetches weather data for current city input."""
        self.hide_error()
        query = self.entry_city.get().strip()

        # Input Validation: Reject empty city input
        if not query:
            self.show_error("Please enter a city name or ZIP code.")
            return

        success, data = weather_service.get_weather(query)
        if not success:
            self.show_error(str(data))
            return

        self.current_data = data
        self._update_display()

    def toggle_units(self):
        """Switches display unit between °C and °F."""
        self.unit = "imperial" if self.unit == "metric" else "metric"
        if self.current_data:
            self._update_display()

    def _update_display(self):
        if not self.current_data:
            return

        d = self.current_data
        is_metric = (self.unit == "metric")

        # Update Hero Panel
        self.lbl_city.config(text=f"{d['city']}, {d['country']}")
        temp_val = d['temp_c'] if is_metric else d['temp_f']
        unit_str = "°C" if is_metric else "°F"
        self.lbl_temp.config(text=f"{temp_val:.1f} {unit_str}")
        self.lbl_condition.config(text=f"{d['icon']} {d['condition']}")
        self.lbl_humidity.config(text=f"💧 Humidity: {d['humidity']}%")

        wind_val = f"{d['wind_speed_kmh']} km/h" if is_metric else f"{d['wind_speed_mph']} mph"
        self.lbl_wind.config(text=f"💨 Wind Speed: {wind_val}")
        self.lbl_source.config(text=f"📡 Source: {d['source']}")

        # Update Hourly Forecast Cards
        for w in self.hourly_container.winfo_children():
            w.destroy()

        for h in d.get('hourly', []):
            card = tk.Frame(self.hourly_container, bg="#FFFFFF", bd=1, relief=tk.RIDGE, padx=12, pady=8)
            card.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=4)

            tk.Label(card, text=h['time'], font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#718096").pack()
            tk.Label(card, text=h['icon'], font=("Segoe UI", 16), bg="#FFFFFF").pack(pady=2)

            t_val = h['temp_c'] if is_metric else h['temp_f']
            tk.Label(card, text=f"{t_val:.1f}{unit_str}", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#2D3748").pack()

        # Update Daily Forecast Cards
        for w in self.daily_container.winfo_children():
            w.destroy()

        for dy in d.get('daily', []):
            dcard = tk.Frame(self.daily_container, bg="#FFFFFF", bd=1, relief=tk.RIDGE, padx=15, pady=10)
            dcard.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

            tk.Label(dcard, text=dy['day'], font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#2B6CB0").pack()
            tk.Label(dcard, text=dy['date'][5:], font=("Segoe UI", 8), bg="#FFFFFF", fg="#A0AEC0").pack()
            tk.Label(dcard, text=dy['icon'], font=("Segoe UI", 20), bg="#FFFFFF").pack(pady=4)

            max_val = dy['temp_max_c'] if is_metric else dy['temp_max_f']
            min_val = dy['temp_min_c'] if is_metric else dy['temp_min_f']

            tk.Label(dcard, text=f"Max: {max_val:.1f}{unit_str}", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#E53E3E").pack()
            tk.Label(dcard, text=f"Min: {min_val:.1f}{unit_str}", font=("Segoe UI", 9), bg="#FFFFFF", fg="#3182CE").pack()
            tk.Label(dcard, text=dy['condition'], font=("Segoe UI", 8), bg="#FFFFFF", fg="#4A5568").pack(pady=(4, 0))

    def show_title_card(self):
        """Displays a static 2-second Title Card window formatted for demo video recording."""
        card_win = tk.Toplevel(self.root)
        card_win.title("OASIS INFOBYTE SIP — Demo Title Card")
        card_win.geometry("600x400")
        card_win.configure(bg="#1A202C")
        card_win.grab_set()

        frame = tk.Frame(card_win, bg="#1A202C", padx=30, pady=30)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="OASIS INFOBYTE SIP", font=("Segoe UI", 16, "bold"), fg="#CBD5E0", bg="#1A202C").pack(pady=(10, 5))
        tk.Label(frame, text="TASK 4 — BASIC WEATHER APP", font=("Segoe UI", 20, "bold"), fg="#63B3ED", bg="#1A202C").pack(pady=(0, 20))

        info_box = tk.Frame(frame, bg="#2D3748", padx=20, pady=20)
        info_box.pack(fill=tk.X, pady=10)

        tk.Label(info_box, text="Full Name: Faizan Sayyed", font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Assigned Track: Python Programming", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Project: Basic Weather App", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)

        timer_lbl = tk.Label(frame, text="Static Title Card (Auto-closes in 2s)...", font=("Segoe UI", 10, "italic"), fg="#A0AEC0", bg="#1A202C")
        timer_lbl.pack(pady=(15, 0))

        # Auto close after 2000 ms (2 seconds)
        card_win.after(2000, card_win.destroy)

def main():
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
