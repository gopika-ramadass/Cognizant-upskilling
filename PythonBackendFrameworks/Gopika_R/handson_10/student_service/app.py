"""
Student Microservice (Port 5002)
Owns the Student domain and students.db SQLite database.
Performs synchronous inter-service calls to Course Service (Port 5001) for enrollment verification.
"""

import os
import sqlite3
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), "students.db")
COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            course_title TEXT,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    # Seed initial student if empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO students (id, name, email) VALUES (?, ?, ?)",
            (1, "Gopika R", "gopika@example.com")
        )
    conn.commit()
    conn.close()


init_db()


@app.route("/api/students/", methods=["GET"])
def list_students():
    """GET /api/students/ — List all students."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    students = [dict(row) for row in rows]
    return jsonify(students), 200


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """GET /api/students/<id> — Get specific student details."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": f"Student with ID {student_id} not found"}), 404

    student = dict(row)
    # Include enrollments
    cursor.execute("SELECT * FROM enrollments WHERE student_id = ?", (student_id,))
    enrollments = [dict(e) for e in cursor.fetchall()]
    student["enrollments"] = enrollments
    conn.close()
    return jsonify(student), 200


@app.route("/api/students/", methods=["POST"])
def create_student():
    """POST /api/students/ — Create a new student."""
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Missing required fields: name, email"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": f"Email {email} already registered"}), 409

    cursor.execute("SELECT * FROM students WHERE id = ?", (new_id,))
    new_student = dict(cursor.fetchone())
    conn.close()
    return jsonify(new_student), 201


# ---------------------------------------------------------------------------------
# Task 2 - Steps 100 & 101: Inter-Service Communication & Fault Tolerance
# ---------------------------------------------------------------------------------
@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    """
    POST /api/students/<id>/enroll (Task 2 - Step 100):
    1. Validates student exists in local DB.
    2. Synchronously calls Course Service (GET http://localhost:5001/api/courses/<course_id>)
       using Python `requests` library.
    3. Handles 503 Service Unavailable if Course Service is unreachable (Step 101).
    """
    data = request.get_json() or {}
    course_id = data.get("course_id")

    if not course_id:
        return jsonify({"error": "Missing required field: course_id"}), 400

    # 1. Verify student exists locally
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student is None:
        conn.close()
        return jsonify({"error": f"Student with ID {student_id} not found"}), 404

    # 2. Inter-service call to Course Service (Task 2 - Step 100 & 101)
    try:
        course_response = requests.get(
            f"{COURSE_SERVICE_URL}/api/courses/{course_id}",
            timeout=3.0
        )
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        conn.close()
        # Step 101: Return 503 Service Unavailable with descriptive error message
        return jsonify({
            "error": "Course Service is currently unavailable. Please try again later.",
            "status_code": 503
        }), 503

    if course_response.status_code == 404:
        conn.close()
        return jsonify({"error": f"Course with ID {course_id} does not exist"}), 404
    elif course_response.status_code != 200:
        conn.close()
        return jsonify({"error": "Failed to verify course with Course Service"}), 500

    course_data = course_response.json()
    course_title = course_data.get("title", "Unknown Course")

    # 3. Record enrollment in local DB
    cursor.execute(
        "INSERT INTO enrollments (student_id, course_id, course_title) VALUES (?, ?, ?)",
        (student_id, course_id, course_title)
    )
    conn.commit()
    enrollment_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student enrolled successfully",
        "enrollment_id": enrollment_id,
        "student_id": student_id,
        "student_name": student["name"],
        "course_id": course_id,
        "course_title": course_title
    }), 201


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "Student Service", "status": "UP", "port": 5002}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
