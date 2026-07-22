import sys
import os

# Add flask_coursemanager to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'flask_coursemanager')))

from app import create_app
from courses.routes import courses_db

def test_flask_api():
    print("=== Task 1 & 2: Testing Flask Application & Blueprint Routes ===")
    app = create_app()
    client = app.test_client()

    # Clear in-memory DB
    courses_db.clear()

    # 1. Test GET /api/courses/ (initial empty array)
    res = client.get('/api/courses/')
    print("1. GET /api/courses/ status:", res.status_code, "Data:", res.get_json())
    assert res.status_code == 200
    assert res.get_json() == []

    # 2. Test POST /api/courses/ with missing fields (should return 400)
    res = client.post('/api/courses/', json={'name': 'Data Structures'})
    print("2. POST missing fields status:", res.status_code, "Error Payload:", res.get_json())
    assert res.status_code == 400
    assert res.get_json()['status'] == 'error'

    # 3. Test POST /api/courses/ with valid payload (should return 201)
    valid_payload = {'name': 'Data Structures & Algorithms', 'code': 'CS101', 'credits': 4}
    res = client.post('/api/courses/', json=valid_payload)
    print("3. POST valid payload status:", res.status_code, "Envelope:", res.get_json())
    assert res.status_code == 201
    assert res.get_json()['status'] == 'success'
    course_id = res.get_json()['data']['id']

    # 4. Test GET /api/courses/<id>/
    res = client.get(f'/api/courses/{course_id}/')
    print("4. GET /api/courses/1/ status:", res.status_code, "Course Name:", res.get_json()['data']['name'])
    assert res.status_code == 200
    assert res.get_json()['data']['code'] == 'CS101'

    # 5. Test PUT /api/courses/<id>/
    res = client.put(f'/api/courses/{course_id}/', json={'credits': 5})
    print("5. PUT /api/courses/1/ status:", res.status_code, "Updated Credits:", res.get_json()['data']['credits'])
    assert res.status_code == 200
    assert res.get_json()['data']['credits'] == 5

    # 6. Test DELETE /api/courses/<id>/
    res = client.delete(f'/api/courses/{course_id}/')
    print("6. DELETE /api/courses/1/ status:", res.status_code)
    assert res.status_code == 200

    # 7. Test GET unknown course ID (should return 404 JSON)
    res = client.get('/api/courses/999/')
    print("7. GET unknown ID status:", res.status_code, "JSON Payload:", res.get_json())
    assert res.status_code == 404
    assert res.get_json()['status'] == 'error'

    # 8. Test 404 JSON error handler for invalid URL
    res = client.get('/api/invalid-route')
    print("8. 404 Handler status:", res.status_code, "JSON Payload:", res.get_json())
    assert res.status_code == 404
    assert res.get_json()['error_code'] == 404

    print("\nALL FLASK HANDS-ON 4 TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_flask_api()
