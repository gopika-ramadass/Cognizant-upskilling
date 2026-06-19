-- 1NF Check
-- Verify that atomic columns do not contain multiple values
SELECT student_id, first_name, email
FROM students
WHERE email LIKE '%,%'
   OR first_name LIKE '%,%';

-- 2NF Check
-- Verify there are no duplicate student-course combinations
SELECT student_id, course_id, COUNT(*) AS enrollment_count
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

-- 3NF Check
-- Verify students reference departments only through department_id
SELECT student_id, department_id
FROM students
WHERE department_id IS NULL;

-- 3NF ANALYSIS
-- The enrollments table satisfies 3NF.
-- 1. enrollment_id uniquely identifies each record.
-- 2. student_id, course_id, enrollment_date, and grade depend only on enrollment_id.
-- 3. No non-key attribute depends on another non-key attribute.
-- 4. There are no transitive dependencies.
-- Therefore, the table structure is in Third Normal Form (3NF).