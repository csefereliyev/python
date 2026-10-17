
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score REAL NOT NULL CHECK(score >= 0 AND score <= 100)
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    connection = get_db()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    score_text = request.form.get("score", "").strip()

    if not name or not score_text:
        return "Введите имя и балл!", 400

    try:
        score = float(score_text.replace(",", "."))
    except ValueError:
        return "Балл должен быть числом!", 400

    if not 0 <= score <= 100:
        return "Балл должен быть от 0 до 100!", 400

    connection = get_db()

    connection.execute(
        "INSERT INTO students (name, score) VALUES (?, ?)",
        (name, score)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
