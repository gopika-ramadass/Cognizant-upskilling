import mysql.connector
import time

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="college_db"
)

cursor = connection.cursor()

print("=" * 60)
print("VERSION 1 : N + 1 Problem")
print("=" * 60)

start = time.time()

query_count = 0

cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()

query_count += 1

for enrollment in enrollments:

    student_id = enrollment[1]

    cursor.execute(
        "SELECT first_name,last_name FROM students WHERE student_id=%s",
        (student_id,)
    )

    student = cursor.fetchone()

    query_count += 1

    print(student[0], student[1])

end = time.time()

print("\nQueries Executed :", query_count)
print("Time :", end-start)


# Single JOIN Solution
print("\n")
print("=" * 60)
print("VERSION 2 : Optimized JOIN")
print("=" * 60)

start = time.time()

query_count = 0

cursor.execute("""

SELECT
s.first_name,
s.last_name,
c.course_name,
e.grade

FROM enrollments e

JOIN students s
ON e.student_id=s.student_id

JOIN courses c
ON e.course_id=c.course_id

""")

rows = cursor.fetchall()

query_count += 1

for row in rows:
    print(row)

end = time.time()

print("\nQueries Executed :", query_count)
print("Time :", end-start)

cursor.close()
connection.close()




# N + 1 Problem Explanation

# Version 1

# 1 Query:
# Fetch all enrollments.

# Then,
# for every enrollment another query is executed
# to retrieve the student's information.

# If there are 12 enrollments,

# Total Queries

# 1 + 12 = 13 Queries

# This is called the N+1 Query Problem.


# Version 2

# A single JOIN query retrieves

# • Student Name
# • Course Name
# • Grade

# using only ONE database query.

# Total Queries = 1


# Real World Scenario

# If there are 10,000 enrollments,

# N+1 Version

# 1 + 10,000

# =

# 10,001 Queries

# Optimized JOIN Version

# Only

# 1 Query

# Therefore JOIN (or eager loading in ORM) significantly reduces
# database round-trips and improves application performance.

