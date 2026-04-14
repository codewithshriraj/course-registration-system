# Course Registration System (DBMS Mini Project)

A full-stack DBMS mini project developed using SDLC principles.

## Tech Stack
- Frontend: HTML, CSS, JavaScript (Fetch API)
- Backend: Python Flask
- Database: MySQL

## Project Structure
- `app.py` - Flask backend and REST APIs
- `templates/index.html` - Main UI
- `static/css/styles.css` - Styling
- `static/js/app.js` - Frontend logic and API calls
- `database/schema.sql` - Database and table creation
- `database/seed.sql` - Optional sample data
- `docs/project_report.md` - Full SDLC report

## APIs Implemented
- POST `/add_student`
- POST `/add_course`
- GET `/courses`
- POST `/register_course`
- POST `/drop_course`
- GET `/registrations`
- DELETE `/delete_student/<student_id>` (optional)
- DELETE `/delete_course/<course_id>` (optional)

## Local Setup (Windows)
1. Make sure MySQL server is running.
2. Run the SQL schema:
   - Open MySQL client and run `database/schema.sql`
   - Optional: run `database/seed.sql`
3. Create and activate virtual environment:
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Start backend:
   - `python app.py`
6. Open browser:
   - `http://127.0.0.1:5000`

## MySQL Credentials Used
- User: `root`
- Password: `shri@123`
- Database: `course_db`

You can override defaults using environment variables from `.env.example`.
