from flask import Blueprint, request, jsonify
from extensions import db
from courses.models import Course, Student, Enrollment, Department

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code=200):
    """
    Helper function to return consistent JSON envelope.
    Envelope: {'status': 'success', 'data': data}
    """
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def get_courses():
    """
    GET /api/courses/
    Queries database for all courses and returns a list of dictionaries using to_dict().
    """
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200


@courses_bp.route('/', methods=['POST'])
def create_course():
    """
    POST /api/courses/
    Creates a new Course object in the database and commits it.
    """
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid or missing JSON payload'}), 400

    required_fields = ['name', 'code', 'credits']
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]

    if missing_fields:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400

    new_course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data.get('department_id')
    )
    db.session.add(new_course)
    db.session.commit()

    return make_response_json(new_course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """
    GET /api/courses/<int:course_id>/
    Uses Course.query.get_or_404(course_id) to retrieve course or return 404 JSON automatically.
    """
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict(), 200)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    """
    PUT /api/courses/<int:course_id>/
    Updates an existing course in the database.
    """
    course = Course.query.get_or_404(course_id)
    data = request.get_json() or {}

    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = data.get('credits', course.credits)
    if 'department_id' in data:
        course.department_id = data['department_id']

    db.session.commit()
    return make_response_json(course.to_dict(), 200)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    """
    DELETE /api/courses/<int:course_id>/
    Deletes course from the database.
    """
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': f'Course {course.name} deleted successfully'}, 200)


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_course_students(course_id):
    """
    GET /api/courses/<int:course_id>/students/
    Uses a JOIN query (Student -> Enrollment) to return all students enrolled in the specified course.
    """
    course = Course.query.get_or_404(course_id)
    enrolled_students = Student.query.join(Enrollment).filter(Enrollment.course_id == course_id).all()
    
    return make_response_json([student.to_dict() for student in enrolled_students], 200)
