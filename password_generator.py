import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string

# Try to import pyperclip; fallback to tkinter clipboard if not available
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # Style configuration (fallback fonts if Segoe UI missing)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabelframe", background="#f0f4f8", foreground="#1e2a3e")
        style.configure("TLabelframe.Label", background="#f0f4f8", foreground="#1e2a3e",
                        font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), background="#ffffff", relief="flat")
        style.map("TButton", background=[("active", "#e2e8f0")])
        style.configure("TLabel", background="#f0f4f8", foreground="#1e2a3e",
                        font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#f0f4f8", font=("Segoe UI", 10))
        style.configure("TScale", background="#f0f4f8")

        # Variables
        self.length = tk.IntVar(value=16)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        # Character sets (original, before filtering)
        self.raw_upper = string.ascii_uppercase
        self.raw_lower = string.ascii_lowercase
        self.raw_digits = string.digits
        self.raw_symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
        self.ambiguous_chars = "il1Lo0O"

        # UI Elements
        self.create_widgets()
        self.generate_password()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # --- Password display ---
        display_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding=(10, 5))
        display_frame.pack(fill="x", pady=(0, 15))

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(display_frame, textvariable=self.password_var,
                                        font=("Consolas", 12), state="readonly")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.copy_btn = ttk.Button(display_frame, text="📋 Copy", command=self.copy_to_clipboard)
        self.copy_btn.pack(side="right")

        # --- Length slider ---
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding=(10, 5))
        length_frame.pack(fill="x", pady=(0, 15))

        self.length_slider = ttk.Scale(length_frame, from_=4, to=50, orient="horizontal",
                                       variable=self.length, command=self.on_length_change)
        self.length_slider.pack(fill="x", padx=5, pady=5)

        self.length_label = ttk.Label(length_frame, text=f"Length: {self.length.get()}")
        self.length_label.pack()

        # --- Character sets checkboxes ---
        chars_frame = ttk.LabelFrame(main_frame, text="Character Sets", padding=(10, 5))
        chars_frame.pack(fill="x", pady=(0, 15))

        ttk.Checkbutton(chars_frame, text="Uppercase (A-Z)", variable=self.use_upper,
                        command=self.generate_password).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(chars_frame, text="Lowercase (a-z)", variable=self.use_lower,
                        command=self.generate_password).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(chars_frame, text="Digits (0-9)", variable=self.use_digits,
                        command=self.generate_password).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(chars_frame, text="Symbols (!@#...)", variable=self.use_symbols,
                        command=self.generate_password).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(chars_frame, text="Exclude ambiguous (il1Lo0O)", variable=self.exclude_ambiguous,
                        command=self.generate_password).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        # --- Strength meter ---
        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", padding=(10, 5))
        strength_frame.pack(fill="x", pady=(0, 15))

        self.strength_progress = ttk.Progressbar(strength_frame, length=400, mode="determinate")
        self.strength_progress.pack(pady=5)
        self.strength_label = ttk.Label(strength_frame, text="")
        self.strength_label.pack()

        # --- Action buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(button_frame, text="🔄 Refresh", command=self.generate_password).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side="right", padx=5)

    def on_length_change(self, event=None):
        self.length_label.config(text=f"Length: {int(self.length.get())}")
        self.generate_password()

    # ---------- Helper: get filtered character set ----------
    def _get_filtered_set(self, raw_set):
        """Return raw_set minus ambiguous characters if exclusion is enabled."""
        if self.exclude_ambiguous.get():
            # remove each ambiguous char from the set
            for ch in self.ambiguous_chars:
                raw_set = raw_set.replace(ch, "")
        return raw_set

    def build_character_pool(self):
        """Return the combined character pool after applying exclusions."""
        pool = ""
        if self.use_upper.get():
            pool += self._get_filtered_set(self.raw_upper)
        if self.use_lower.get():
            pool += self._get_filtered_set(self.raw_lower)
        if self.use_digits.get():
            pool += self._get_filtered_set(self.raw_digits)
        if self.use_symbols.get():
            pool += self._get_filtered_set(self.raw_symbols)
        return pool

    def generate_password(self):
        """Generate a secure random password."""
        pool = self.build_character_pool()
        length = int(self.length.get())

        # No character set selected
        if not pool:
            self.password_var.set("Please select at least one character set")
            self.strength_progress["value"] = 0
            self.strength_label.config(text="No character sets selected", foreground="gray")
            return

        # Ensure at least one character from each selected set (filtered)
        password_chars = []
        if self.use_upper.get():
            filtered_upper = self._get_filtered_set(self.raw_upper)
            if filtered_upper:   # may become empty after exclusion
                password_chars.append(secrets.choice(filtered_upper))
        if self.use_lower.get():
            filtered_lower = self._get_filtered_set(self.raw_lower)
            if filtered_lower:
                password_chars.append(secrets.choice(filtered_lower))
        if self.use_digits.get():
            filtered_digits = self._get_filtered_set(self.raw_digits)
            if filtered_digits:
                password_chars.append(secrets.choice(filtered_digits))
        if self.use_symbols.get():
            filtered_symbols = self._get_filtered_set(self.raw_symbols)
            if filtered_symbols:
                password_chars.append(secrets.choice(filtered_symbols))

        # If after filtering some sets became empty, we may have fewer guaranteed chars.
        # Fill the rest with random choices from the full pool.
        remaining = length - len(password_chars)
        if remaining > 0:
            for _ in range(remaining):
                password_chars.append(secrets.choice(pool))
        else:
            # Length shorter than number of chosen sets? Trim the list.
            password_chars = password_chars[:length]

        # Shuffle to avoid predictable order
        secrets.SystemRandom().shuffle(password_chars)

        password = "".join(password_chars)
        self.password_var.set(password)
        self.update_strength_meter(pool, length)

    def update_strength_meter(self, pool, length):
        """Evaluate strength using entropy estimation."""
        if not pool:
            return

        pool_size = len(pool)
        # entropy in bits: length * log2(pool_size)
        # use bit_length for fast log2 approximation
        if pool_size <= 1:
            entropy = 0
        else:
            entropy = length * (pool_size.bit_length() - 1)

        if entropy < 30:
            strength = "Very Weak"
            value = 20
            color = "#e53e3e"
        elif entropy < 50:
            strength = "Weak"
            value = 40
            color = "#ed8936"
        elif entropy < 70:
            strength = "Moderate"
            value = 60
            color = "#ecc94b"
        elif entropy < 90:
            strength = "Strong"
            value = 80
            color = "#48bb78"
        else:
            strength = "Very Strong"
            value = 100
            color = "#38a169"

        self.strength_progress["value"] = value
        self.strength_label.config(text=f"{strength} (entropy ~{entropy} bits)", foreground=color)

    def copy_to_clipboard(self):
        """Copy password to clipboard with fallback if pyperclip missing."""
        password = self.password_var.get()
        if not password or "Please select" in password:
            messagebox.showwarning("Nothing to copy", "Generate a valid password first.")
            return

        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
        else:
            # Fallback: use tkinter's clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # keeps clipboard after app closes

        messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()