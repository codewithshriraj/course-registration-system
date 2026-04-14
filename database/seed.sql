USE course_db;

INSERT INTO students (student_id, full_name, email, phone_number, branch, semester)
VALUES
('S001', 'Aarav Sharma', 'aarav.sharma@example.com', '9876543210', 'Computer Science', 'Semester 4'),
('S002', 'Neha Iyer', 'neha.iyer@example.com', '9876501234', 'Information Technology', 'Semester 6')
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name);

INSERT INTO courses (course_id, course_name, instructor_name, credits, department)
VALUES
('C101', 'Database Management Systems', 'Dr. Kumar', 4, 'CSE'),
('C102', 'Web Technologies', 'Prof. Mehta', 3, 'CSE')
ON DUPLICATE KEY UPDATE course_name = VALUES(course_name);
