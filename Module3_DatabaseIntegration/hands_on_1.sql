-- #Create Database
CREATE DATABASE college_db;

USE college_db;

-- #Departments Table
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- #Students Table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id)
	REFERENCES departments(department_id)
);

-- #Courses Table
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id)
	REFERENCES departments(department_id)
);

-- #Enrollments Table
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id)
	REFERENCES students(student_id),
    FOREIGN KEY (course_id)
	REFERENCES courses(course_id)
);

-- #professors Table
CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id)
	REFERENCES departments(department_id)
);

#task -2 

# 1NF Check
# Verify that atomic columns do not contain multiple values
SELECT student_id, first_name, email
FROM students
WHERE email LIKE '%,%'
   OR first_name LIKE '%,%';

#2NF Check
#Verify there are no duplicate student-course combinations
SELECT student_id, course_id, COUNT(*) AS enrollment_count
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

#3NF Check
#Verify students reference departments only through department_id
SELECT student_id, department_id
FROM students
WHERE department_id IS NULL;

# 3NF ANALYSIS
#The enrollments table satisfies 3NF.
# 1. enrollment_id uniquely identifies each record.
# 2. student_id, course_id, enrollment_date, and grade depend only on enrollment_id.
# 3. No non-key attribute depends on another non-key attribute.
# 4. There are no transitive dependencies.
# Therefore, the table structure is in Third Normal Form (3NF).

#task -3 

-- Add phone number column
ALTER TABLE students
ADD phone_number VARCHAR(15);

-- Add max seats column
ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

-- Add CHECK constraint on grade
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (
    grade IN ('A','B','C','D','F')
    OR grade IS NULL
);

-- Rename hod_name column
ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

-- Drop phone number column
ALTER TABLE students
DROP COLUMN phone_number;