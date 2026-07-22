from flask import Flask, jsonify, request
from flask import Response
import json

app = Flask(__name__)

# ─── In-memory storage ────────────────────────────────────────────────────────
courses_db = {}
course_counter = 1

# ─── Helper: Standard Error Response ─────────────────────────────────────────
def error_response(code: str, message: str, field=None, status_code=400):
    """
    Standardised error envelope format:
    {'error': {'code': 'NOT_FOUND', 'message': '...', 'field': null}}
    """
    return jsonify({'error': {'code': code, 'message': message, 'field': field}}), status_code


# ─── Helper: Pagination Envelope ──────────────────────────────────────────────
def paginate(items, page, per_page, base_url):
    """
    Returns offset-based pagination envelope:
    {'count': total, 'next': url|null, 'previous': url|null, 'results': [...]}
    """
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]

    next_url = f"{base_url}?page={page + 1}&per_page={per_page}" if end < total else None
    prev_url = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None

    return {
        'count': total,
        'next': next_url,
        'previous': prev_url,
        'results': page_items
    }


# ─── API v1 Routes ─────────────────────────────────────────────────────────────

@app.get('/api/v1/courses/')
def get_courses():
    """
    GET /api/v1/courses/
    URL versioning: /api/v1/ prefix ensures backward compatibility.
    Supports: ?page, ?per_page (offset pagination), ?search (case-insensitive filter)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str).lower()

    all_courses = list(courses_db.values())

    # Case-insensitive search on name or code
    if search:
        all_courses = [c for c in all_courses if search in c['name'].lower() or search in c['code'].lower()]

    result = paginate(all_courses, page, per_page, '/api/v1/courses/')
    return jsonify(result), 200


@app.post('/api/v1/courses/')
def create_course():
    """
    POST /api/v1/courses/
    Returns 201 Created with Location header pointing to new resource.
    """
    global course_counter
    data = request.get_json() or {}
    required = ['name', 'code', 'credits']
    missing = [f for f in required if f not in data]
    if missing:
        return error_response('VALIDATION_ERROR', f"Missing required fields: {', '.join(missing)}", field=missing[0], status_code=400)

    new_course = {'id': course_counter, 'name': data['name'], 'code': data['code'], 'credits': data['credits']}
    courses_db[course_counter] = new_course
    course_counter += 1

    response = jsonify({'status': 'success', 'data': new_course})
    response.status_code = 201
    # Location header points to the newly created resource
    response.headers['Location'] = f"/api/v1/courses/{new_course['id']}/"
    return response


@app.get('/api/v1/courses/<int:course_id>/')
def get_course(course_id):
    if course_id not in courses_db:
        return error_response('NOT_FOUND', f'Course with id {course_id} not found', status_code=404)
    return jsonify({'status': 'success', 'data': courses_db[course_id]}), 200


@app.put('/api/v1/courses/<int:course_id>/')
def update_course(course_id):
    """
    PUT /api/v1/courses/<id>/
    Full replacement of course resource.
    """
    if course_id not in courses_db:
        return error_response('NOT_FOUND', f'Course with id {course_id} not found', status_code=404)

    data = request.get_json() or {}
    required = ['name', 'code', 'credits']
    missing = [f for f in required if f not in data]
    if missing:
        return error_response('VALIDATION_ERROR', f"Missing required fields: {', '.join(missing)}", field=missing[0], status_code=400)

    courses_db[course_id] = {'id': course_id, 'name': data['name'], 'code': data['code'], 'credits': data['credits']}
    return jsonify({'status': 'success', 'data': courses_db[course_id]}), 200


@app.patch('/api/v1/courses/<int:course_id>/')
def partial_update_course(course_id):
    """
    PATCH /api/v1/courses/<id>/
    Partial update: only provided fields are modified (unlike PUT which requires all fields).
    """
    if course_id not in courses_db:
        return error_response('NOT_FOUND', f'Course with id {course_id} not found', status_code=404)

    data = request.get_json() or {}
    course = courses_db[course_id]
    course['name'] = data.get('name', course['name'])
    course['code'] = data.get('code', course['code'])
    course['credits'] = data.get('credits', course['credits'])

    return jsonify({'status': 'success', 'data': course}), 200


@app.delete('/api/v1/courses/<int:course_id>/')
def delete_course(course_id):
    if course_id not in courses_db:
        return error_response('NOT_FOUND', f'Course with id {course_id} not found', status_code=404)
    courses_db.pop(course_id)
    return '', 204


# ─── Custom JSON Error Handlers ────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return error_response('NOT_FOUND', 'Requested resource or URL was not found', status_code=404)

@app.errorhandler(405)
def method_not_allowed(e):
    return error_response('METHOD_NOT_ALLOWED', 'HTTP method not allowed on this endpoint', status_code=405)

@app.errorhandler(500)
def internal_error(e):
    return error_response('INTERNAL_ERROR', 'Internal Server Error', status_code=500)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
