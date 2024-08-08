import json
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import re
import hashlib

# Encryption and Decryption Functions
def generate_key():
    """Generate a key and save it to a file."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """Load the previously generated key."""
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """Encrypt the message."""
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    """Decrypt the message."""
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

def hash_password(password):
    """Hash the master password."""
    return hashlib.sha256(password.encode()).hexdigest()

def set_master_password(password):
    """Save the hashed master password."""
    with open("master_password.txt", "w") as file:
        file.write(hash_password(password))

def verify_master_password(password):
    """Verify the entered master password."""
    try:
        with open("master_password.txt", "r") as file:
            stored_hash = file.read()
        return hash_password(password) == stored_hash
    except FileNotFoundError:
        return False

# Password Strength Check
def is_strong_password(password):
    """Check the strength of the password."""
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# JSON File Handling
def save_password(username, password):
    """Save or update the username and encrypted password in a JSON file."""
    data = {}
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    # Encrypt and save the password
    encrypted_password = encrypt_message(password)
    data[username] = encrypted_password.decode()

    # Save the updated data back to the file
    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

def load_password(username):
    """Load and decrypt the password for the given username."""
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
        encrypted_password = data.get(username)
        if encrypted_password:
            return decrypt_message(encrypted_password.encode())
    except FileNotFoundError:
        pass
    return None

# GUI Implementation
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Setup GUI elements for master password
        self.master_password_label = tk.Label(root, text="Master Password:")
        self.master_password_label.pack()
        
        self.master_password_entry = tk.Entry(root, show="*")
        self.master_password_entry.pack()
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        # Setup GUI elements for managing passwords
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        
        self.save_button = tk.Button(root, text="Save Password", command=self.save_password)
        self.save_button.pack()
        
        self.edit_button = tk.Button(root, text="Edit Password", command=self.edit_password)
        self.edit_button.pack()
        
        self.load_button = tk.Button(root, text="Load Password", command=self.load_password)
        self.load_button.pack()
        
        self.view_all_button = tk.Button(root, text="View All Passwords", command=self.view_all_passwords)
        self.view_all_button.pack()
        
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
        self.show_elements(False)

    def login(self):
        master_password = self.master_password_entry.get()
        if verify_master_password(master_password):
            self.show_elements(True)
            self.master_password_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Login Error", "Incorrect master password.")

    def show_elements(self, show):
        """Show or hide elements based on authentication."""
        elements = [self.username_label, self.username_entry, self.password_label, self.password_entry,
                    self.save_button, self.edit_button, self.load_button, self.view_all_button, self.result_label]
        for element in elements:
            element.pack() if show else element.pack_forget()

    def save_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not is_strong_password(password):
            messagebox.showinfo("Password Strength", "Password is weak, but will be saved.")
        
        save_password(username, password)
        messagebox.showinfo("Password Saved", "Password has been saved.")
        
    def edit_password(self):
        username = self.username_entry.get()
        new_password = self.password_entry.get()
        
        if load_password(username) is not None:
            if not is_strong_password(new_password):
                messagebox.showinfo("Password Strength", "Password is weak, but will be updated.")
            
            save_password(username, new_password)
            messagebox.showinfo("Password Updated", "Password has been updated.")
        else:
            messagebox.showinfo("Error", "No password found for this username.")
        
    def load_password(self):
        username = self.username_entry.get()
        password = load_password(username)
        if password:
            self.result_label.config(text=f"Password: {password}")
        else:
            self.result_label.config(text="No password found.")
    
    def view_all_passwords(self):
        """View all stored passwords."""
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
            all_passwords = "\n".join(f"{user}: {decrypt_message(pwd.encode())}" for user, pwd in data.items())
            self.result_label.config(text=f"All Passwords:\n{all_passwords}")
        except FileNotFoundError:
            self.result_label.config(text="No passwords found.")

if __name__ == "__main__":
    # Generate and save the key if not already done
    try:
        load_key()
    except FileNotFoundError:
        generate_key()

    # Prompt for master password setup
    if not verify_master_password("dummy"):  # Check if master password is already set
        master_password = input("Set the master password: ")
        set_master_password(master_password)
    
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
