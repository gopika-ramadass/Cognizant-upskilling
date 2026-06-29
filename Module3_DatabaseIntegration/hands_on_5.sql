
-- HANDS-ON 4
-- Query Optimisation – Indexes, EXPLAIN & the N+1 Problem

USE college_db;

-- TASK 1 : Baseline Performance (Without Indexes)

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;


-- Sample Observation
--
-- Before creating indexes:
--
-- 1. students table performs Full Table Scan.
-- 2. enrollments table performs Full Table Scan.
-- 3. courses table may use PRIMARY KEY.
-- 4. Query cost is higher because every row is scanned.
--
-- Note:
-- Full Table Scan is acceptable for very small tables,
-- but becomes expensive as the table size increases.


-- TASK 2 : Create Indexes


-- Step 51
CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);


-- Step 52
CREATE UNIQUE INDEX idx_enrollment_student_course
ON enrollments(student_id, course_id);


-- Step 53
CREATE INDEX idx_course_code
ON courses(course_code);


-- Step 54
EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;


-- Observation after indexing
--
-- students table now uses idx_students_enrollment_year
-- instead of Full Table Scan.
--
-- JOIN operations become faster.
--
-- Less number of rows are examined.
--
-- Overall query performance improves.


-- STEP 55
-- Partial Index


-- PostgreSQL

CREATE INDEX idx_null_grade
ON enrollments(student_id)
WHERE grade IS NULL;



-- MySQL Alternative
--
-- MySQL doesn't support partial indexes.
-- Instead create a normal index.
--
-- CREATE INDEX idx_null_grade
-- ON enrollments(student_id, grade);


-- Testing Composite Unique Index


-- This duplicate insert should fail.

INSERT INTO enrollments
(student_id, course_id, enrollment_date, grade)
VALUES
(1,1,'2022-07-01','A');

-- Expected:
-- Duplicate entry error due to UNIQUE INDEX.