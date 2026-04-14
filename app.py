import os
import re
import time
from datetime import date

from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "course_db"),
    )


def validate_student_payload(data):
    required_fields = [
        "student_id",
        "full_name",
        "email",
        "phone_number",
        "branch",
        "semester",
    ]
    for field in required_fields:
        if not str(data.get(field, "")).strip():
            return f"{field} is required"

    if not EMAIL_REGEX.match(data["email"]):
        return "Invalid email format"

    return None


def validate_course_payload(data):
    required_fields = ["course_id", "course_name", "instructor_name", "credits", "department"]
    for field in required_fields:
        if not str(data.get(field, "")).strip():
            return f"{field} is required"

    try:
        credits = int(data["credits"])
        if credits <= 0:
            return "credits must be a positive integer"
    except (ValueError, TypeError):
        return "credits must be an integer"

    return None


@app.route("/")
def home():
    return render_template("index.html", asset_version=int(time.time()))


@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    validation_error = validate_student_payload(data)
    if validation_error:
        return jsonify({"success": False, "message": validation_error}), 400

    query = """
        INSERT INTO students (student_id, full_name, email, phone_number, branch, semester)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data["student_id"].strip(),
        data["full_name"].strip(),
        data["email"].strip(),
        data["phone_number"].strip(),
        data["branch"].strip(),
        data["semester"].strip(),
    )

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"success": True, "message": "Student added successfully"}), 201
    except Error as err:
        message = "Database error"
        if err.errno == 1062:
            message = "Student ID or email already exists"
        return jsonify({"success": False, "message": message, "error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/add_course", methods=["POST"])
def add_course():
    data = request.get_json(silent=True) or {}
    validation_error = validate_course_payload(data)
    if validation_error:
        return jsonify({"success": False, "message": validation_error}), 400

    query = """
        INSERT INTO courses (course_id, course_name, instructor_name, credits, department)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data["course_id"].strip(),
        data["course_name"].strip(),
        data["instructor_name"].strip(),
        int(data["credits"]),
        data["department"].strip(),
    )

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"success": True, "message": "Course added successfully"}), 201
    except Error as err:
        message = "Database error"
        if err.errno == 1062:
            message = "Course ID already exists"
        return jsonify({"success": False, "message": message, "error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/courses", methods=["GET"])
def get_courses():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses ORDER BY course_id")
        courses = cursor.fetchall()
        return jsonify({"success": True, "data": courses}), 200
    except Error as err:
        return jsonify({"success": False, "message": "Could not fetch courses", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/register_course", methods=["POST"])
def register_course():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    course_id = str(data.get("course_id", "")).strip()

    if not student_id or not course_id:
        return jsonify({"success": False, "message": "student_id and course_id are required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Student not found"}), 404

        cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Course not found"}), 404

        cursor.execute(
            """
            SELECT registration_id FROM registrations
            WHERE student_id = %s AND course_id = %s AND status = 'Registered'
            """,
            (student_id, course_id),
        )
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Duplicate registration is not allowed"}), 409

        insert_query = """
            INSERT INTO registrations (student_id, course_id, registration_date, status)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (student_id, course_id, date.today(), "Registered"))
        conn.commit()

        return jsonify({"success": True, "message": "Course registered successfully"}), 201
    except Error as err:
        return jsonify({"success": False, "message": "Registration failed", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/drop_course", methods=["POST"])
def drop_course():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    course_id = str(data.get("course_id", "")).strip()

    if not student_id or not course_id:
        return jsonify({"success": False, "message": "student_id and course_id are required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        update_query = """
            UPDATE registrations
            SET status = 'Dropped'
            WHERE student_id = %s AND course_id = %s AND status = 'Registered'
        """
        cursor.execute(update_query, (student_id, course_id))

        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "No active registration found to drop"}), 404

        conn.commit()
        return jsonify({"success": True, "message": "Course dropped successfully"}), 200
    except Error as err:
        return jsonify({"success": False, "message": "Drop operation failed", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/registrations", methods=["GET"])
def get_registrations():
    student_id = request.args.get("student_id", "").strip()

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        base_query = """
            SELECT
                r.registration_id,
                r.student_id,
                s.full_name,
                r.course_id,
                c.course_name,
                r.registration_date,
                r.status
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
        """

        params = ()
        if student_id:
            base_query += " WHERE r.student_id = %s"
            params = (student_id,)

        base_query += " ORDER BY r.registration_id DESC"
        cursor.execute(base_query, params)
        rows = cursor.fetchall()

        return jsonify({"success": True, "data": rows}), 200
    except Error as err:
        return jsonify({"success": False, "message": "Could not fetch registrations", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/delete_student/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Student not found"}), 404
        conn.commit()
        return jsonify({"success": True, "message": "Student deleted successfully"}), 200
    except Error as err:
        return jsonify({"success": False, "message": "Delete failed", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/delete_course/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Course not found"}), 404
        conn.commit()
        return jsonify({"success": True, "message": "Course deleted successfully"}), 200
    except Error as err:
        return jsonify({"success": False, "message": "Delete failed", "error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "True").lower() == "true",
    )
