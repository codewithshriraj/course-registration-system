# Course Registration System

A full-stack course registration web application built with Flask and MySQL.

## Features
- Add students and courses
- Register and drop courses
- View available courses and registrations
- Simple browser-based UI for DBMS mini project demos

## Tech Stack
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: MySQL

## Project Structure
- `app.py`: Flask app and API routes
- `templates/index.html`: Main UI page
- `static/css/styles.css`: Frontend styling
- `static/js/app.js`: Frontend behavior and API calls
- `database/schema.sql`: Database schema
- `database/seed.sql`: Optional seed data
- `requirements.txt`: Python dependencies

## API Endpoints
- `POST /add_student`
- `POST /add_course`
- `GET /courses`
- `POST /register_course`
- `POST /drop_course`
- `GET /registrations`
- `DELETE /delete_student/<student_id>`
- `DELETE /delete_course/<course_id>`

## Setup (Windows)
1. Ensure MySQL server is running.
2. Create the database schema:
   - Run `database/schema.sql`
   - Optionally run `database/seed.sql`
3. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Run the app:
   - `python app.py`
6. Open in browser:
   - `http://127.0.0.1:5000`

## Configuration
Use environment variables for database credentials. A sample is provided in `.env.example`.

## License
This project is licensed under the MIT License. See `LICENSE` for details.
