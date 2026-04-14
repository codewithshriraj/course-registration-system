CREATE DATABASE IF NOT EXISTS course_db;
USE course_db;

CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    branch VARCHAR(80) NOT NULL,
    semester VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(120) NOT NULL,
    instructor_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    department VARCHAR(80) NOT NULL,
    CONSTRAINT chk_credits_positive CHECK (credits > 0)
);

CREATE TABLE IF NOT EXISTS registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(20) NOT NULL,
    registration_date DATE NOT NULL,
    status ENUM('Registered', 'Dropped') NOT NULL DEFAULT 'Registered',
    CONSTRAINT fk_reg_student
        FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_reg_course
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_student_course_status (student_id, course_id, status)
);
