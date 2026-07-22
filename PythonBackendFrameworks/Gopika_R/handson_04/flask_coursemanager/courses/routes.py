from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory courses store for Hands-On 4
courses_db = {}
course_id_counter = 1

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
    Returns list of all courses in JSON format.
    """
    return jsonify([course for course in courses_db.values()]), 200


@courses_bp.route('/', methods=['POST'])
def create_course():
    """
    POST /api/courses/
    Parses request body, validates required fields (name, code, credits), and creates a course.
    """
    global course_id_counter
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

    new_course = {
        'id': course_id_counter,
        'name': data['name'],
        'code': data['code'],
        'credits': data['credits']
    }
    courses_db[course_id_counter] = new_course
    course_id_counter += 1

    return make_response_json(new_course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """
    GET /api/courses/<int:course_id>/
    Retrieves course by ID or raises 404.
    """
    if course_id not in courses_db:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404

    return make_response_json(courses_db[course_id], 200)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    """
    PUT /api/courses/<int:course_id>/
    Updates existing course by ID.
    """
    if course_id not in courses_db:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404

    data = request.get_json() or {}
    course = courses_db[course_id]

    course['name'] = data.get('name', course['name'])
    course['code'] = data.get('code', course['code'])
    course['credits'] = data.get('credits', course['credits'])

    return make_response_json(course, 200)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    """
    DELETE /api/courses/<int:course_id>/
    Deletes course by ID.
    """
    if course_id not in courses_db:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404

    deleted = courses_db.pop(course_id)
    return make_response_json({'message': f'Course {deleted["name"]} deleted successfully'}, 200)
