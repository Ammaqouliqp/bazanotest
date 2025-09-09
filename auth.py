from flask import Flask, render_template, request, redirect, url_for, flash
from .database import get_db_connection
from .logs import log_event
from .models import init_db

# Initialize DB tables
init_db()

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ------------------ ROUTES ------------------

@app.route("/", methods=["GET"])
def index():
    return render_template("auth.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("index") + "#signup")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        flash("Username already exists.", "error")
        log_event(username, "signup", "failure", "user already exists")
        conn.close()
        return redirect(url_for("index") + "#signup")

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    flash("Signup successful! You can now login.", "success")
    log_event(username, "signup", "success")
    return redirect(url_for("index") + "#login")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        flash(f"Welcome, {username}!", "success")
        log_event(username, "login", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid username or password.", "error")
        log_event(username, "login", "failure", "incorrect credentials")
        return redirect(url_for("index") + "#login")


@app.route("/dashboard")
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == "__main__":
    app.run(debug=True)
