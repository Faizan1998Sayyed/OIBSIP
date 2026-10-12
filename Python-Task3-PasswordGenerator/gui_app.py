"""
GUI Application for Random Password Generator (Advanced Tier)
Tkinter GUI with sliders, spinboxes, checkboxes, visual strength bar, clipboard integration, and session history.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import generator_logic

# Optional pyperclip import with safe fallback to tkinter clipboard
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🔐 Cryptographically Secure Password Generator")
        self.root.geometry("680x640")
        self.root.minsize(620, 580)
        self.root.configure(bg="#F7FAFC")

        # In-Memory History (last 5 passwords, not saved to disk for security)
        self.history = []

        # Configure custom TTK styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()

        # Build UI Layout
        self._build_ui()
        self.on_generate() # Initial generation on app launch

    def _configure_styles(self):
        bg_color = "#F7FAFC"
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=bg_color, foreground="#2D3748")

        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1A202C", background=bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#718096", background=bg_color)
        self.style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"), foreground="#4A5568", background=bg_color)
        self.style.configure("TCheckbutton", font=("Segoe UI", 10), background=bg_color, foreground="#2D3748")

        # Primary Generate Button
        self.style.configure("Generate.TButton", font=("Segoe UI", 11, "bold"), background="#3182CE", foreground="#FFFFFF")
        self.style.map("Generate.TButton", background=[("active", "#2B6CB0")])

        # Copy Button
        self.style.configure("Copy.TButton", font=("Segoe UI", 10, "bold"), background="#38A169", foreground="#FFFFFF")
        self.style.map("Copy.TButton", background=[("active", "#2F855A")])

        # Progress bar custom
        self.style.configure("Strength.Horizontal.TProgressbar", thickness=12)

    def _build_ui(self):
        # Header Frame
        header_frame = ttk.Frame(self.root, padding="15 15 15 10")
        header_frame.pack(fill=tk.X)

        title_inner = ttk.Frame(header_frame)
        title_inner.pack(side=tk.LEFT, fill=tk.X, expand=True)

        title = ttk.Label(title_inner, text="🔐 RANDOM PASSWORD GENERATOR", style="Header.TLabel")
        title.pack(anchor=tk.W)

        subtitle = ttk.Label(title_inner, text="Cryptographically Secure CS PRNG (secrets module) • Zero Disk Persistence", style="SubHeader.TLabel")
        subtitle.pack(anchor=tk.W)

        # Title Card Button for Demo Video (OASIS INFOBYTE requirement)
        btn_title_card = ttk.Button(header_frame, text="🎬 Demo Title Card (2s)", command=self.show_title_card)
        btn_title_card.pack(side=tk.RIGHT, padx=5)

        # Output Password & Copy Section
        output_frame = ttk.LabelFrame(self.root, text=" Generated Password ", padding="15")
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        out_inner = ttk.Frame(output_frame)
        out_inner.pack(fill=tk.X)

        self.entry_password = ttk.Entry(out_inner, font=("Consolas", 14, "bold"), justify="center")
        self.entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        btn_copy = ttk.Button(out_inner, text="📋 Copy", style="Copy.TButton", command=self.on_copy_to_clipboard)
        btn_copy.pack(side=tk.RIGHT)

        # Strength Bar & Status Label
        strength_frame = ttk.Frame(output_frame, padding="0 10 0 0")
        strength_frame.pack(fill=tk.X)

        self.lbl_strength = ttk.Label(strength_frame, text="Strength: —", font=("Segoe UI", 10, "bold"))
        self.lbl_strength.pack(side=tk.LEFT)

        self.lbl_entropy = ttk.Label(strength_frame, text="Entropy: 0.0 bits", font=("Segoe UI", 9), foreground="#718096")
        self.lbl_entropy.pack(side=tk.RIGHT)

        self.progress_strength = ttk.Progressbar(output_frame, style="Strength.Horizontal.TProgressbar", maximum=100)
        self.progress_strength.pack(fill=tk.X, pady=(5, 0))

        # Settings Controls Frame
        settings_frame = ttk.LabelFrame(self.root, text=" Password Controls & Criteria ", padding="15")
        settings_frame.pack(fill=tk.X, padx=15, pady=5)

        # Length Slider + Spinbox
        len_frame = ttk.Frame(settings_frame)
        len_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(len_frame, text="Password Length (min 8):", style="Field.TLabel").pack(side=tk.LEFT, padx=(0, 10))

        self.spin_length = ttk.Spinbox(len_frame, from_=8, to=64, width=5, font=("Segoe UI", 10, "bold"), command=self.on_spin_changed)
        self.spin_length.pack(side=tk.RIGHT, padx=(10, 0))
        self.spin_length.set(16)

        self.slider_length = ttk.Scale(len_frame, from_=8, to=64, orient=tk.HORIZONTAL, command=self.on_slider_moved)
        self.slider_length.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.slider_length.set(16)

        # Checkboxes for Character Types
        chk_frame = ttk.Frame(settings_frame)
        chk_frame.pack(fill=tk.X, pady=5)

        self.var_upper = tk.BooleanVar(value=True)
        self.var_lower = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=True)
        self.var_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(chk_frame, text="Uppercase (A-Z)", variable=self.var_upper, command=self.on_criteria_changed).grid(row=0, column=0, sticky=tk.W, padx=10, pady=4)
        ttk.Checkbutton(chk_frame, text="Lowercase (a-z)", variable=self.var_lower, command=self.on_criteria_changed).grid(row=0, column=1, sticky=tk.W, padx=10, pady=4)
        ttk.Checkbutton(chk_frame, text="Numbers (0-9)", variable=self.var_digits, command=self.on_criteria_changed).grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
        ttk.Checkbutton(chk_frame, text="Symbols (!@#$...)", variable=self.var_symbols, command=self.on_criteria_changed).grid(row=1, column=1, sticky=tk.W, padx=10, pady=4)
        ttk.Checkbutton(chk_frame, text="Exclude Ambiguous (0, O, l, 1, I, |)", variable=self.var_ambiguous, command=self.on_criteria_changed).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=4)

        # Generate Button
        btn_generate = ttk.Button(settings_frame, text="⚡ GENERATE NEW PASSWORD", style="Generate.TButton", command=self.on_generate)
        btn_generate.pack(fill=tk.X, pady=(15, 0))

        # Session History (Last 5 Passwords) Frame
        history_frame = ttk.LabelFrame(self.root, text=" Session History (Last 5 Passwords — Memory Only) ", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("password", "length", "strength")
        self.tree_history = ttk.Treeview(history_frame, columns=columns, show="headings", height=5)
        self.tree_history.heading("password", text="Generated Password")
        self.tree_history.heading("length", text="Length")
        self.tree_history.heading("strength", text="Strength")

        self.tree_history.column("password", width=350, anchor=tk.W)
        self.tree_history.column("length", width=80, anchor=tk.CENTER)
        self.tree_history.column("strength", width=140, anchor=tk.CENTER)

        self.tree_history.pack(fill=tk.BOTH, expand=True)
        self.tree_history.bind("<Double-1>", self.on_history_double_click)

        # Status Bar Footer
        self.lbl_status = ttk.Label(self.root, text="Ready", style="SubHeader.TLabel", padding="10 5")
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

    def on_slider_moved(self, val):
        length = int(float(val))
        self.spin_length.set(length)

    def on_spin_changed(self):
        try:
            val = int(self.spin_length.get())
            if val < 8:
                val = 8
            if val > 64:
                val = 64
            self.slider_length.set(val)
        except ValueError:
            pass

    def on_criteria_changed(self):
        pass

    def on_generate(self):
        try:
            length = int(self.spin_length.get())
        except ValueError:
            messagebox.showwarning("Validation Error", "Length must be a valid integer.")
            return

        success, pwd_or_err = generator_logic.generate_password(
            length=length,
            use_upper=self.var_upper.get(),
            use_lower=self.var_lower.get(),
            use_digits=self.var_digits.get(),
            use_symbols=self.var_symbols.get(),
            exclude_ambiguous=self.var_ambiguous.get()
        )

        if not success:
            messagebox.showwarning("Input Criteria Error", pwd_or_err)
            return

        # Display password
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, pwd_or_err)

        # Calculate strength
        strength = generator_logic.calculate_strength(
            pwd_or_err,
            self.var_upper.get(),
            self.var_lower.get(),
            self.var_digits.get(),
            self.var_symbols.get(),
            self.var_ambiguous.get()
        )

        self.progress_strength['value'] = strength['score']
        self.lbl_strength.config(text=f"Strength: {strength['label']}")
        self.lbl_entropy.config(text=f"Entropy: {strength['entropy']} bits")

        # Auto Copy on generation
        self.copy_to_clipboard_silent(pwd_or_err)

        # Update History
        self.history.insert(0, {'password': pwd_or_err, 'length': len(pwd_or_err), 'strength': strength['label']})
        if len(self.history) > 5:
            self.history.pop()

        self._refresh_history_tree()
        self.lbl_status.config(text=f"✅ New password generated & auto-copied to clipboard!")

    def copy_to_clipboard_silent(self, text: str):
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(text)
                return
            except Exception:
                pass
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def on_copy_to_clipboard(self):
        pwd = self.entry_password.get()
        if not pwd:
            return
        self.copy_to_clipboard_silent(pwd)
        self.lbl_status.config(text="📋 Password copied to clipboard!")
        messagebox.showinfo("Copied!", "Password successfully copied to clipboard.")

    def _refresh_history_tree(self):
        for item in self.tree_history.get_children():
            self.tree_history.delete(item)

        for item in self.history:
            self.tree_history.insert("", tk.END, values=(item['password'], item['length'], item['strength']))

    def on_history_double_click(self, event):
        selected = self.tree_history.selection()
        if selected:
            vals = self.tree_history.item(selected[0], "values")
            if vals:
                pwd = vals[0]
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, pwd)
                self.lbl_status.config(text="📋 Selected password copied from history!")

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
        tk.Label(frame, text="TASK 3 — PASSWORD GENERATOR", font=("Segoe UI", 20, "bold"), fg="#68D391", bg="#1A202C").pack(pady=(0, 20))

        info_box = tk.Frame(frame, bg="#2D3748", padx=20, pady=20)
        info_box.pack(fill=tk.X, pady=10)

        tk.Label(info_box, text="Full Name: Faizan Sayyed", font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Assigned Track: Python Programming", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)
        tk.Label(info_box, text="Project: Random Password Generator", font=("Segoe UI", 12), fg="#E2E8F0", bg="#2D3748").pack(anchor=tk.W, pady=4)

        timer_lbl = tk.Label(frame, text="Static Title Card (Auto-closes in 2s)...", font=("Segoe UI", 10, "italic"), fg="#A0AEC0", bg="#1A202C")
        timer_lbl.pack(pady=(15, 0))

        # Auto close after 2000 ms (2 seconds)
        card_win.after(2000, card_win.destroy)

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
