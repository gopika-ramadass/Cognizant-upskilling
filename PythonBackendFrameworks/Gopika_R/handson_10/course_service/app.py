"""
Course Microservice (Port 5001)
Owns the Course domain and courses.db SQLite database.
"""

import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), "courses.db")


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            credits INTEGER DEFAULT 3
        )
    """)
    # Seed initial course if empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO courses (id, title, code, department, credits) VALUES (?, ?, ?, ?, ?)",
            (101, "Microservices & Distributed Systems", "CS501", "Computer Science", 4)
        )
        cursor.execute(
            "INSERT INTO courses (id, title, code, department, credits) VALUES (?, ?, ?, ?, ?)",
            (102, "Cloud Native Architecture", "CS502", "Computer Science", 3)
        )
    conn.commit()
    conn.close()


init_db()


@app.route("/api/courses/", methods=["GET"])
def list_courses():
    """GET /api/courses/ — List all courses."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    conn.close()
    courses = [dict(row) for row in rows]
    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """GET /api/courses/<id> — Get specific course details."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404
    return jsonify(dict(row)), 200


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """POST /api/courses/ — Create a new course."""
    data = request.get_json() or {}
    title = data.get("title")
    code = data.get("code")
    department = data.get("department")
    credits = data.get("credits", 3)

    if not title or not code or not department:
        return jsonify({"error": "Missing required fields: title, code, department"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO courses (title, code, department, credits) VALUES (?, ?, ?, ?)",
            (title, code, department, credits)
        )
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": f"Course code {code} already exists"}), 409

    cursor.execute("SELECT * FROM courses WHERE id = ?", (new_id,))
    new_course = dict(cursor.fetchone())
    conn.close()
    return jsonify(new_course), 201


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """DELETE /api/courses/<id> — Delete a course."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Course {course_id} deleted successfully"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "Course Service", "status": "UP", "port": 5001}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
