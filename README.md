# 🔐 Advanced Password Generator

A modern and secure Password Generator built with Python and Tkinter. This desktop application allows users to generate strong, customizable passwords with real-time strength analysis and clipboard support.

## 📌 Features

### ✅ Secure Password Generation
- Uses Python's `secrets` module for cryptographically secure random passwords.
- More secure than using the standard `random` module.

### ✅ Customizable Password Options
Users can:
- Include Uppercase Letters (A-Z)
- Include Lowercase Letters (a-z)
- Include Numbers (0-9)
- Include Special Symbols (!@#$%^&*)
- Exclude Ambiguous Characters (e.g., `l`, `I`, `1`, `O`, `0`)

### ✅ Password Length Control
- Adjustable password length from **4 to 50 characters**.
- Interactive slider for easy selection.

### ✅ Password Strength Meter
Displays password strength based on:
- Password length
- Character pool size
- Estimated entropy

Strength Levels:
- Very Weak
- Weak
- Moderate
- Strong
- Very Strong

### ✅ Copy to Clipboard
- One-click password copy feature.
- Supports both:
  - `pyperclip`
  - Tkinter clipboard fallback

### ✅ Modern GUI
- Clean and responsive user interface.
- Built using Tkinter and ttk widgets.

---

## 🛠️ Technologies Used

- Python 3.x
- Tkinter
- ttk Widgets
- Secrets Module
- String Module
- Pyperclip (Optional)

---

## 📂 Project Structure
