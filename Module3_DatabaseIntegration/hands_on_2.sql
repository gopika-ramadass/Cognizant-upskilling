
/* 
   TASK 1: INSERT, UPDATE, DELETE
*/

/* Insert 2 additional students */
INSERT INTO students
(first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES
('Gopika', 'Ramadass', 'gopika.r@college.edu', '2005-03-08', 1, 2024),
('Rahul', 'Kumar', 'rahul.k@college.edu', '2004-06-15', 2, 2024);

/* Update grade */
UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5
AND course_id = 1;

/* Preview NULL grades before delete */
SELECT *
FROM enrollments
WHERE grade IS NULL;

/* Delete NULL grades */
DELETE FROM enrollments
WHERE grade IS NULL;

/* Verify row counts */
SELECT COUNT(*) AS student_count
FROM students;

SELECT COUNT(*) AS enrollment_count
FROM enrollments;


/*
   TASK 2: SINGLE TABLE QUERIES
*/

/* Students enrolled in 2022 */
SELECT *
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

/* Courses with more than 3 credits */
SELECT *
FROM courses
WHERE credits > 3
ORDER BY credits DESC;

/* Professors with salary between 80000 and 95000 */
SELECT *
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

/* Students whose email ends with @college.edu */
SELECT *
FROM students
WHERE email LIKE '%@college.edu';

/* Count students per enrollment year */
SELECT
    enrollment_year,
    COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year;


/* 
   TASK 3: MULTI-TABLE JOINS
*/

/* Student name and department */
SELECT
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    d.dept_name
FROM students s
INNER JOIN departments d
ON s.department_id = d.department_id;

/* Enrollment with student and course details */
SELECT
    e.enrollment_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.course_name,
    e.grade
FROM enrollments e
INNER JOIN students s
ON e.student_id = s.student_id
INNER JOIN courses c
ON e.course_id = c.course_id;

/* Students not enrolled in any course */
SELECT
    s.student_id,
    s.first_name,
    s.last_name
FROM students s
LEFT JOIN enrollments e
ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

/* Course-wise student count including courses with zero enrollments */
SELECT
    c.course_name,
    COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

/* Department, professors and salary */
SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id;


/* 
   TASK 4: AGGREGATIONS
*/

/* Total enrollments per course */
SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

/* Average professor salary per department */
SELECT
    d.dept_name,
    ROUND(AVG(p.salary), 2) AS average_salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id
GROUP BY d.department_id, d.dept_name;

/* Departments with budget greater than 600000 */
SELECT *
FROM departments
WHERE budget > 600000;

/* Grade distribution for CS101 */
SELECT
    e.grade,
    COUNT(*) AS grade_count
FROM enrollments e
INNER JOIN courses c
ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

/* Departments having more than 2 students */
SELECT
    d.dept_name,
    COUNT(s.student_id) AS total_students
FROM departments d
INNER JOIN students s
ON d.department_id = s.department_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(s.student_id) > 2;