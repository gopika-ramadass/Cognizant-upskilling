"""
API Gateway Microservice (Port 5000)
Implements the API Gateway pattern by routing requests to downstream services:
- /api/courses/*  → Course Service (Port 5001)
- /api/students/* → Student Service (Port 5002)
"""

import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL", "http://localhost:5002")


def proxy_request(target_base_url, path):
    """Generic HTTP proxy function using requests.request() (Task 2 - Step 102)."""
    target_url = f"{target_base_url}/{path}"
    
    # Forward headers excluding Host
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            cookies=request.cookies,
            allow_redirects=False,
            timeout=5.0
        )
        
        # Filter response headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                            if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, response_headers)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return Response(
            '{"error": "Target microservice is unavailable or unreachable", "status_code": 503}',
            status=503,
            mimetype='application/json'
        )


@app.route('/api/courses/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def courses_proxy(path):
    """Route /api/courses/* → Course Service (Port 5001)."""
    full_path = f"api/courses/{path}" if path else "api/courses/"
    return proxy_request(COURSE_SERVICE_URL, full_path)


@app.route('/api/students/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def students_proxy(path):
    """Route /api/students/* → Student Service (Port 5002)."""
    full_path = f"api/students/{path}" if path else "api/students/"
    return proxy_request(STUDENT_SERVICE_URL, full_path)


@app.route('/health', methods=['GET'])
def health():
    return {
        "gateway": "API Gateway",
        "status": "UP",
        "port": 5000,
        "routes": {
            "/api/courses/*": COURSE_SERVICE_URL,
            "/api/students/*": STUDENT_SERVICE_URL
        }
    }, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
