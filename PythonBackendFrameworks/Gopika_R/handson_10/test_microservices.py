"""
Pytest Suite for Hands-On 10: Microservices Architecture
Verifies independent service execution, inter-service communication,
503 Service Unavailable handling when Course Service is unreachable,
and API Gateway proxy routing.
"""

import sys
import os
import pytest
from unittest.mock import patch
import requests

# Add microservice directories to sys.path for direct testing
sys.path.append(os.path.join(os.path.dirname(__file__), "course_service"))
sys.path.append(os.path.join(os.path.dirname(__file__), "student_service"))
sys.path.append(os.path.join(os.path.dirname(__file__), "gateway"))

from course_service.app import app as course_app
from student_service.app import app as student_app
from gateway.app import app as gateway_app


@pytest.fixture
def course_client():
    course_app.config['TESTING'] = True
    with course_app.test_client() as client:
        yield client


@pytest.fixture
def student_client():
    student_app.config['TESTING'] = True
    with student_app.test_client() as client:
        yield client


@pytest.fixture
def gateway_client():
    gateway_app.config['TESTING'] = True
    with gateway_app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------------
# Task 1 Tests: Decomposed Microservice Operations
# ---------------------------------------------------------------------------------
def test_course_service_independent_endpoints(course_client):
    """Step 99: Verify course_service endpoints work independently."""
    # 1. Get course list
    res = course_client.get("/api/courses/")
    assert res.status_code == 200
    assert isinstance(res.json, list)

    # 2. Get existing course (ID 101 seeded)
    res_single = course_client.get("/api/courses/101")
    assert res_single.status_code == 200
    assert res_single.json["code"] == "CS501"

    # 3. Non-existent course 404
    res_404 = course_client.get("/api/courses/99999")
    assert res_404.status_code == 404


def test_student_service_independent_endpoints(student_client):
    """Step 99: Verify student_service endpoints work independently."""
    # 1. Get student list
    res = student_client.get("/api/students/")
    assert res.status_code == 200
    assert isinstance(res.json, list)

    # 2. Get existing student (ID 1 seeded)
    res_single = student_client.get("/api/students/1")
    assert res_single.status_code == 200
    assert res_single.json["name"] == "Gopika R"


# ---------------------------------------------------------------------------------
# Task 2 Tests: Inter-Service Calls & Fault Tolerance
# ---------------------------------------------------------------------------------
def test_enrollment_inter_service_success(student_client):
    """Step 100: Verify student_service calls course_service to verify course during enrollment."""
    mock_course_response = requests.Response()
    mock_course_response.status_code = 200
    mock_course_response._content = b'{"id": 101, "title": "Microservices & Distributed Systems"}'

    with patch("student_service.app.requests.get", return_value=mock_course_response) as mock_get:
        response = student_client.post(
            "/api/students/1/enroll",
            json={"course_id": 101}
        )
        assert response.status_code == 201
        data = response.json
        assert data["message"] == "Student enrolled successfully"
        assert data["course_title"] == "Microservices & Distributed Systems"
        mock_get.assert_called_once()


def test_enrollment_service_unavailable_returns_503(student_client):
    """Step 101: Verify student_service handles Course Service connection failure by returning 503."""
    with patch("student_service.app.requests.get", side_effect=requests.exceptions.ConnectionError("Connection refused")):
        response = student_client.post(
            "/api/students/1/enroll",
            json={"course_id": 101}
        )
        assert response.status_code == 503
        data = response.json
        assert "Course Service is currently unavailable" in data["error"]
        assert data["status_code"] == 503


# ---------------------------------------------------------------------------------
# Task 2 Tests: API Gateway Pattern Proxying
# ---------------------------------------------------------------------------------
def test_api_gateway_routing_to_downstream_services(gateway_client):
    """Steps 102 & 103: Verify API Gateway routes /api/courses/* and /api/students/*."""
    mock_downstream_resp = requests.Response()
    mock_downstream_resp.status_code = 200
    mock_downstream_resp._content = b'[{"id": 101, "title": "Microservices & Distributed Systems"}]'
    mock_downstream_resp.raw = requests.packages.urllib3.response.HTTPResponse(
        body=b'[{"id": 101, "title": "Microservices & Distributed Systems"}]',
        headers={'Content-Type': 'application/json'}
    )

    with patch("gateway.app.requests.request", return_value=mock_downstream_resp) as mock_req:
        res = gateway_client.get("/api/courses/")
        assert res.status_code == 200
        mock_req.assert_called_once()
        args, kwargs = mock_req.call_args
        assert kwargs["method"] == "GET"
        assert "http://localhost:5001/api/courses/" in kwargs["url"]
