import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'flask_coursemanager')))

from app import create_app
from extensions import db
from courses.models import Department, Course, Student, Enrollment

def test_sqlalchemy_app():
    print("=== Task 1 & 2: Testing Flask with SQLAlchemy ORM & Database Integration ===")
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

        # Step 51: Insert 2 departments and 3 courses via ORM
        dept1 = Department(name='Computer Science', head_of_dept='Alan Turing', budget=50000.0)
        dept2 = Department(name='Electrical Engineering', head_of_dept='Nikola Tesla', budget=45000.0)
        db.session.add_all([dept1, dept2])
        db.session.commit()

        c1 = Course(name='Data Structures', code='CS101', credits=4, department_id=dept1.id)
        c2 = Course(name='Algorithms', code='CS102', credits=4, department_id=dept1.id)
        c3 = Course(name='Circuit Analysis', code='EE101', credits=3, department_id=dept2.id)
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        s1 = Student(first_name='Alice', last_name='Smith', email='alice@example.com', department_id=dept1.id, enrollment_year=2024)
        s2 = Student(first_name='Bob', last_name='Jones', email='bob@example.com', department_id=dept1.id, enrollment_year=2024)
        db.session.add_all([s1, s2])
        db.session.commit()

        e1 = Enrollment(student_id=s1.id, course_id=c1.id, grade='A')
        db.session.add(e1)
        db.session.commit()

        print(f"Database Seeded: {Department.query.count()} departments, {Course.query.count()} courses, {Student.query.count()} students.")

    # Step 52: Test GET /api/courses/
    res = client.get('/api/courses/')
    print("1. GET /api/courses/ status:", res.status_code, "Count:", len(res.get_json()))
    assert res.status_code == 200
    assert len(res.get_json()) == 3

    # Step 54: Test POST /api/courses/ (Creates & commits Course via ORM)
    new_course_data = {'name': 'Operating Systems', 'code': 'CS103', 'credits': 4, 'department_id': 1}
    res = client.post('/api/courses/', json=new_course_data)
    print("2. POST /api/courses/ status:", res.status_code, "Created Course:", res.get_json()['data'])
    assert res.status_code == 201
    assert res.get_json()['data']['code'] == 'CS103'

    # Step 55: Test GET /api/courses/<id>/ with get_or_404
    res = client.get('/api/courses/1/')
    print("3. GET /api/courses/1/ status:", res.status_code, "Course Name:", res.get_json()['data']['name'])
    assert res.status_code == 200

    res = client.get('/api/courses/999/')
    print("4. GET /api/courses/999/ (404 test) status:", res.status_code)
    assert res.status_code == 404

    # Step 56: Test GET /api/courses/<id>/students/ (JOIN query)
    res = client.get('/api/courses/1/students/')
    print("5. GET /api/courses/1/students/ JOIN query status:", res.status_code)
    print("   Enrolled Students:", [s['first_name'] + ' ' + s['last_name'] for s in res.get_json()['data']])
    assert res.status_code == 200
    assert len(res.get_json()['data']) == 1
    assert res.get_json()['data'][0]['first_name'] == 'Alice'

    print("\nALL FLASK SQLALCHEMY HANDS-ON 5 TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_sqlalchemy_app()
