"""
API Versioning Strategy Notes
==============================

URL Versioning (Used in this implementation: /api/v1/courses/):
- Pros: Explicit, easy to test in browser, easy to route in reverse proxies (nginx/ALB), cacheable.
- Cons: URL is "polluted" with version info; resource identity changes with version.

Header-based Versioning (Accept: application/vnd.api.v1+json):
- Pros: Clean URLs; version is part of content negotiation (true REST philosophy).
- Cons: Harder to test (need tools like curl/Postman), not visible in browser, caching is trickier.

Decision for this project: URL versioning (/api/v1/) is used for simplicity and explicit visibility.
"""

from app import app, courses_db, course_counter
import app as app_module

def reset():
    courses_db.clear()
    app_module.course_counter = 1

def test_rest_best_practices():
    print("=== Hands-On 8: RESTful API Design Best Practices ===")
    client = app.test_client()
    reset()

    # 1. POST → 201 with Location header
    res = client.post('/api/v1/courses/', json={'name': 'Data Structures', 'code': 'CS101', 'credits': 4})
    print("1. POST /api/v1/courses/ status:", res.status_code)
    assert res.status_code == 201
    assert 'Location' in res.headers
    print("   Location header:", res.headers['Location'])
    assert '/api/v1/courses/1/' in res.headers['Location']
    course_id = res.get_json()['data']['id']

    # 2. GET → 200 with pagination envelope
    for i in range(4):
        client.post('/api/v1/courses/', json={'name': f'Course {i}', 'code': f'C10{i}', 'credits': 3})

    res = client.get('/api/v1/courses/?page=1&per_page=2')
    print("2. GET /api/v1/courses/?page=1&per_page=2 status:", res.status_code)
    data = res.get_json()
    assert res.status_code == 200
    assert 'count' in data and 'next' in data and 'previous' in data and 'results' in data
    assert len(data['results']) == 2
    print("   Pagination envelope count:", data['count'], "next:", data['next'])

    # 3. PATCH → 200 partial update (only credits)
    res = client.patch(f'/api/v1/courses/{course_id}/', json={'credits': 5})
    print("3. PATCH /api/v1/courses/1/ status:", res.status_code, "updated credits:", res.get_json()['data']['credits'])
    assert res.status_code == 200
    assert res.get_json()['data']['credits'] == 5

    # 4. Case-insensitive search
    res = client.get('/api/v1/courses/?search=data')
    print("4. GET ?search=data status:", res.status_code, "results:", len(res.get_json()['results']))
    assert res.status_code == 200
    assert len(res.get_json()['results']) >= 1

    # 5. 404 → standardized error JSON
    res = client.get('/api/v1/courses/9999/')
    print("5. GET nonexistent course status:", res.status_code, "error:", res.get_json()['error']['code'])
    assert res.status_code == 404
    assert res.get_json()['error']['code'] == 'NOT_FOUND'

    # 6. 400 → VALIDATION_ERROR
    res = client.post('/api/v1/courses/', json={'name': 'No Code'})
    print("6. POST missing fields status:", res.status_code, "error:", res.get_json()['error']['code'])
    assert res.status_code == 400
    assert res.get_json()['error']['code'] == 'VALIDATION_ERROR'

    # 7. DELETE → 204 No Content
    res = client.delete(f'/api/v1/courses/{course_id}/')
    print("7. DELETE /api/v1/courses/1/ status:", res.status_code)
    assert res.status_code == 204

    # 8. 404 after delete
    res = client.get(f'/api/v1/courses/{course_id}/')
    print("8. GET after delete status:", res.status_code)
    assert res.status_code == 404

    print("\nALL REST BEST PRACTICES TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_rest_best_practices()
