import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

# ---------- Database Initialization ----------
def init_db():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/")
def quiz():
    return render_template("quiz.html")

@app.route("/submit", methods=["POST"])
def submit():
    score = 0

    if request.form.get("q1") == "a":
        score += 1
    if request.form.get("q2") == "b":
        score += 1
    if request.form.get("q3") == "b":
        score += 1
    if request.form.get("q4") == "b":
        score += 1
    if request.form.get("q5") == "a":
        score += 1

    # Store score in database
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (score) VALUES (?)", (score,))
    conn.commit()
    conn.close()

    return f"""
        <h2>Quiz Submitted Successfully</h2>
        <p>Your Score: <b>{score}/5</b></p>
        <a href="/">Take Quiz Again</a>
    """

# ---------- Run App (Cloud Compatible) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

