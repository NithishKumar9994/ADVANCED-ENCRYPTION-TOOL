import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# === KEY MANAGEMENT ===
KEY_FILE = "encryption.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    return generate_key()

# === FILE OPERATIONS ===
def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(filepath + ".enc", 'wb') as f:
        f.write(encrypted)
    messagebox.showinfo("Success", f"File encrypted: {filepath}.enc")

def decrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()
    try:
        decrypted = fernet.decrypt(encrypted_data)
        new_path = filepath.replace(".enc", ".dec")
        with open(new_path, 'wb') as f:
            f.write(decrypted)
        messagebox.showinfo("Success", f"File decrypted: {new_path}")
    except Exception as e:
        messagebox.showerror("Error", "Decryption failed! File may be corrupted or wrong key.")

# === GUI INTERFACE ===
def browse_encrypt():
    filepath = filedialog.askopenfilename()
    if filepath:
        encrypt_file(filepath)

def browse_decrypt():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if filepath:
        decrypt_file(filepath)

root = tk.Tk()
root.title("🔐 Advanced AES Encryption Tool")
root.geometry("400x200")
root.resizable(False, False)

tk.Label(root, text="Select a file to encrypt or decrypt using AES-256", font=("Segoe UI", 11)).pack(pady=20)

tk.Button(root, text="🔒 Encrypt File", width=20, command=browse_encrypt, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="🔓 Decrypt File", width=20, command=browse_decrypt, bg="#2196F3", fg="white").pack()

tk.Label(root, text="Encryption key saved in: encryption.key", font=("Segoe UI", 9), fg="gray").pack(side="bottom", pady=10)

root.mainloop()
