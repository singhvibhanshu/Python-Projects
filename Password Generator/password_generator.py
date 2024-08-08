import tkinter as tk
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        self.min_length_label = tk.Label(root, text="Minimum length of password:")
        self.min_length_label.pack(pady=5)

        self.min_length_entry = tk.Entry(root)
        self.min_length_entry.pack(pady=5)

        self.include_specials_var = tk.BooleanVar()
        self.include_specials_check = tk.Checkbutton(root, text="Include special characters", variable=self.include_specials_var)
        self.include_specials_check.pack(pady=5)

        self.include_numbers_var = tk.BooleanVar()
        self.include_numbers_check = tk.Checkbutton(root, text="Include numbers", variable=self.include_numbers_var)
        self.include_numbers_check.pack(pady=5)

        self.include_uppercase_var = tk.BooleanVar()
        self.include_uppercase_check = tk.Checkbutton(root, text="Include uppercase letters", variable=self.include_uppercase_var)
        self.include_uppercase_check.pack(pady=5)

        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=10)

        self.password_label = tk.Label(root, text="")
        self.password_label.pack(pady=10)

    def generate_password(self):
        min_length = self.min_length_entry.get()
        if not min_length.isdigit() or int(min_length) <= 0:
            self.password_label.config(text="Invalid length. Please enter a positive number.")
            return

        min_length = int(min_length)
        chars = string.ascii_lowercase

        if self.include_uppercase_var.get():
            chars += string.ascii_uppercase
        if self.include_numbers_var.get():
            chars += string.digits
        if self.include_specials_var.get():
            chars += string.punctuation

        if len(chars) == 0:
            self.password_label.config(text="Please select at least one character type.")
            return

        password = ''.join(random.choice(chars) for _ in range(min_length))
        self.password_label.config(text=f"Generated Password: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
