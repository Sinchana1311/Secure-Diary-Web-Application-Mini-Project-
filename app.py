from flask import Flask, render_template, request, redirect, session, url_for
from cryptography.fernet import Fernet
import os
import hashlib
import random
import string
import time
from functools import wraps

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure random key

DIARY_FILE = "diary_data/diary.txt"
KEY_FILE = "diary_data/key.key"
CREDENTIALS_FILE = "diary_data/credentials.txt"  # Store user credentials
RESET_TOKENS = {}  # Temporary store for reset tokens and their expiration

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

# Hash password function for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if username exists and verify password
def check_credentials(username, password):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            credentials = f.readlines()
            for line in credentials:
                stored_username, stored_password = line.strip().split(":")
                if stored_username == username and stored_password == hash_password(password):
                    return True
    return False

# Save the credentials (username and hashed password)
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")

# Generate a random token for password reset
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Login required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

# Request reset password route
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as f:
                credentials = f.readlines()
                for line in credentials:
                    stored_username, _ = line.strip().split(":")
                    if stored_username == username:
                        token = generate_reset_token()
                        RESET_TOKENS[token] = {
                            "username": username,
                            "expires": time.time() + 3600  # Token expires in 1 hour
                        }
                        reset_link = url_for("reset_password", token=token, _external=True)
                        return render_template("forgot_password.html", reset_link=reset_link)
        return render_template("forgot_password.html", error="Username not found")
    return render_template("forgot_password.html")

# Reset password route
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if token not in RESET_TOKENS or RESET_TOKENS[token]["expires"] < time.time():
        return render_template("reset_password.html", error="Invalid or expired token")
    
    if request.method == "POST":
        new_password = request.form["password"]
        if new_password:
            username = RESET_TOKENS[token]["username"]
            update_password(username, new_password)
            del RESET_TOKENS[token]
            return redirect("/login")
    
    return render_template("reset_password.html", token=token)

def update_password(username, new_password):
    lines = []
    with open(CREDENTIALS_FILE, "r") as f:
        lines = f.readlines()

    with open(CREDENTIALS_FILE, "w") as f:
        for line in lines:
            stored_username, stored_password = line.strip().split(":")
            if stored_username == username:
                f.write(f"{username}:{hash_password(new_password)}\n")
            else:
                f.write(line)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return render_template("register.html", error="Username and Password are required")
        
        save_credentials(username, password)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if check_credentials(username, password):
            session["logged_in"] = True
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        entry = request.form["entry"]
        encrypted = fernet.encrypt(entry.encode())
        with open(DIARY_FILE, "ab") as f:
            f.write(encrypted + b"\n")
        return redirect("/entries")
    return render_template("index.html")

@app.route("/entries")
@login_required
def entries():
    entries = []
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "rb") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    entries.append(fernet.decrypt(line).decode())
                except:
                    entries.append("[Decryption Failed]")
    return render_template("entries.html", entries=entries)

@app.route("/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "rb") as f:
            lines = f.readlines()

        if 0 <= entry_id < len(lines):
            del lines[entry_id]
            with open(DIARY_FILE, "wb") as f:
                f.writelines(lines)

    return redirect("/entries")

if __name__ == "__main__":
    app.run(debug=True)
