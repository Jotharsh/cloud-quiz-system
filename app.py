from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Create database and table (runs once)
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

@app.route("/")
def quiz():
    return render_template("quiz.html")

@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    if request.form.get("q1") == "a":
        score += 1

    # Store score in database
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (score) VALUES (?)", (score,))
    conn.commit()
    conn.close()

    return f"Quiz submitted! Your score is {score}/1 (Saved in database)"

if __name__ == "__main__":
    app.run(debug=True)
