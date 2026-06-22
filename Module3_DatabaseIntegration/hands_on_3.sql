


/* 
   TASK 1 : SUBQUERIES
*/

/* 35. Students enrolled in more courses than average */

SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(e.course_id) AS total_courses
FROM students s
JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_enrollments
);


/* 36. Courses where all enrolled students received grade A */

SELECT
    c.course_id,
    c.course_name,
    c.course_code
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);


/* 37. Highest paid professor in each department */

SELECT
    p.professor_id,
    p.prof_name,
    p.department_id,
    p.salary
FROM professors p
WHERE p.salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);


/* 38. Departments with average salary above 85000 */

SELECT *
FROM
(
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) dept_avg
WHERE avg_salary > 85000;



/* 
   TASK 2 : VIEWS
*/

/* 39. Student Enrollment Summary View */

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS GPA

FROM students s
LEFT JOIN departments d
ON s.department_id = d.department_id

LEFT JOIN enrollments e
ON s.student_id = e.student_id

GROUP BY
s.student_id,
student_name,
d.dept_name;


/* 40. Course Statistics View */

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,

    COUNT(e.enrollment_id) AS total_enrollments,

    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS avg_gpa

FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id

GROUP BY
c.course_id,
c.course_name,
c.course_code;


/* View Output */

SELECT * FROM vw_student_enrollment_summary;

SELECT * FROM vw_course_stats;


/* 41. Students with GPA > 3 */

SELECT *
FROM vw_student_enrollment_summary
WHERE GPA > 3.0;


/* 42. Update through View (for testing) */

UPDATE vw_student_enrollment_summary
SET student_name = 'TEST STUDENT'
WHERE student_id = 1;

/*
Multi-table views containing
JOINs, GROUP BY and aggregate functions
are generally NOT updatable.

Most DBMS systems will throw an error.
*/


/* 43. Drop and recreate view with CHECK OPTION */

DROP VIEW IF EXISTS vw_student_enrollment_summary;

DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    department_id
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

SELECT * FROM vw_student_enrollment_summary;



/* 
   TASK 3 : STORED PROCEDURES & TRANSACTIONS
*/


/* 44. Procedure : Enroll Student */

DELIMITER $$

CREATE PROCEDURE sp_enroll_student
(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN

    IF EXISTS
    (
        SELECT 1
        FROM enrollments
        WHERE student_id = p_student_id
        AND course_id = p_course_id
    )
    THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate Enrollment Not Allowed';

    ELSE

        INSERT INTO enrollments
        (
            student_id,
            course_id,
            enrollment_date
        )
        VALUES
        (
            p_student_id,
            p_course_id,
            p_enrollment_date
        );

    END IF;

END $$

DELIMITER ;


/* Test Procedure */

CALL sp_enroll_student(2,5,'2024-01-15');



/* 45. Transfer Student Procedure */


/* Log Table */

CREATE TABLE IF NOT EXISTS department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student_id INT,
    IN p_new_department INT
)
BEGIN

    DECLARE old_dept INT;

    START TRANSACTION;

    SELECT department_id
    INTO old_dept
    FROM students
    WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_department
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log
    (
        student_id,
        old_department,
        new_department
    )
    VALUES
    (
        p_student_id,
        old_dept,
        p_new_department
    );

    COMMIT;

END $$

DELIMITER ;



/* Test Transfer Procedure */

CALL sp_transfer_student(1,2);



/* 46. Manual Error Test */

/*
Use an invalid department ID.

Expected:
Foreign key error
Transaction should rollback.
*/

CALL sp_transfer_student(1,999);



/* 
   47. SAVEPOINT DEMONSTRATION
*/

START TRANSACTION;


/* First insert */

INSERT INTO enrollments
(
    student_id,
    course_id,
    enrollment_date,
    grade
)
VALUES
(
    1,
    3,
    CURDATE(),
    'A'
);


/* Create savepoint */

SAVEPOINT first_insert;


/* Intentional failure */

INSERT INTO enrollments
(
    student_id,
    course_id,
    enrollment_date,
    grade
)
VALUES
(
    999,
    3,
    CURDATE(),
    'A'
);


/* Rollback only failed portion */

ROLLBACK TO first_insert;


/* Commit successful insert */

COMMIT;


/* Verify */

SELECT *
FROM enrollments
WHERE student_id = 1
AND course_id = 3;