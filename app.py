
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Dummy secret for secret-scanning practice only
DEMO_API_KEY = "demo_key_NOT_A_REAL_SECRET_12345"

def init_db():
    conn = sqlite3.connect("bank.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL
        )
    """)
    conn.execute(
        "INSERT OR IGNORE INTO users VALUES (1, 'alice', 2500.00)"
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return """
    <h1>VulnerableBank - Security Lab</h1>
    <p>Test user: alice</p>
    <form action="/account">
        <input name="username" placeholder="Username">
        <button type="submit">View Account</button>
    </form>
    """

@app.route("/account")

def account():
    username = request.args.get("username", "")

    conn = sqlite3.connect("bank.db")

    # FIX: Use a parameterized query to prevent SQL injection.
    query = (
        "SELECT username, balance FROM users "
        "WHERE username = ?"
    )

    try:
        result = conn.execute(query, (username,)).fetchone()
    except sqlite3.Error:
        result = None
    finally:
        conn.close()

    if result:
        return f"<h2>Account: {result[0]}</h2><p>Balance: {result[1]}</p>"

    return "<h2>Account not found</h2>"


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
