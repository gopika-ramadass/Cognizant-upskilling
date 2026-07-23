# Hands-On 10: Microservices Architecture — Concepts & Decomposition

## Overview
This hands-on exercise decomposes the Course Management Monolith into independent microservices, establishes synchronous inter-service communication with fault-tolerant `503 Service Unavailable` handling, and implements an API Gateway proxy routing layer using **Flask** and **Requests**.

---

## Task 1: Monolith Service Decomposition & Bounded Contexts

### Bounded Context Decomposition Table (Task 1 - Steps 96 & 97)

| Service Name | Responsibility | Endpoints Owned | Database Owned | Port |
| :--- | :--- | :--- | :--- | :--- |
| **Course Service** | Department & Course CRUD, Catalog management | `/api/courses/*` | `courses.db` (SQLite) | `5001` |
| **Student Service** | Student CRUD, Course Enrollment tracking | `/api/students/*` | `students.db` (SQLite) | `5002` |
| **Auth Service** | User registration, login, JWT token verification | `/api/auth/*` | `auth.db` (SQLite) | `5003` |
| **Notification Service** | Email confirmations & event notifications | `/api/notifications/*` | `notifications.db` (SQLite) | `5004` |

### Core Microservice Principles Applied
1. **Database-per-Service:** Each microservice strictly owns its database (`courses.db` for Course Service, `students.db` for Student Service). Direct cross-database queries or shared connections are forbidden.
2. **Independent Deployability:** Each service runs as a standalone Python process on a separate port (`5001` and `5002`).

---

## Task 2: Inter-Service Communication & API Gateway Pattern

### 1. Synchronous Inter-Service Communication (`student_service/app.py`)
- When a client calls `POST /api/students/<id>/enroll` with `{"course_id": 101}`:
  1. Student Service verifies the student exists in `students.db`.
  2. Student Service makes a synchronous HTTP `GET http://localhost:5001/api/courses/101` request to Course Service using Python's `requests` library.
  3. If Course Service returns 200 OK, enrollment is committed to `students.db`.

### 2. Fault Tolerance & Unavailability Handling (`503 Service Unavailable`)
- If Course Service is down or unresponsive:
  - Student Service catches `requests.exceptions.ConnectionError` and `requests.exceptions.Timeout`.
  - Returns **`503 Service Unavailable`** with descriptive payload:
    ```json
    {
      "error": "Course Service is currently unavailable. Please try again later.",
      "status_code": 503
    }
    ```

### 3. API Gateway Pattern (`gateway/app.py` - Port 5000)
- Single ingress Flask application acting as a reverse proxy for all client traffic:
  - `/api/courses/*` → Proxied to Course Service (`http://localhost:5001`)
  - `/api/students/*` → Proxied to Student Service (`http://localhost:5002`)
- Forwards HTTP method, request headers, query string parameters, and JSON payloads seamlessly.

---

## Architecture Deep-Dive & Trade-offs (Task 2 - Step 104)

### 1. Synchronous (HTTP) vs Asynchronous (Message Queue) Communication

| Dimension | Synchronous (HTTP / REST) | Asynchronous (Message Queue: RabbitMQ / Kafka) |
| :--- | :--- | :--- |
| **Coupling** | **Tight coupling** (Caller relies on target service availability). | **Loose coupling** (Services interact via message topics/queues). |
| **Latency** | Immediate real-time response. | Eventual consistency; non-blocking background processing. |
| **Resilience** | High risk of **cascading failures** if a dependency goes down. | High resilience; messages buffer in queue until consumer recovers. |
| **Complexity** | Low complexity (Standard REST endpoints). | Moderate to High operational complexity (Broker management). |

### 2. When to Use Message Queues (RabbitMQ / Kafka)?
- **Non-blocking Operations:** Sending email/SMS notifications, generating PDF receipts, or processing background audit logs.
- **Traffic Spikes & Load Leveling:** Buffering surge incoming requests (e.g. flash sales, ticket reservations) without overloading downstream databases.
- **Event-Driven Workflows:** Emitting domain events (`StudentEnrolled`, `OrderPlaced`) consumed asynchronously by multiple interested services.

### 3. API Gateway Responsibilities in Production
While this exercise demonstrates URL proxy routing, a production API Gateway handles:
1. **Authentication & Token Validation:** Validates JWT tokens centrally before forwarding requests to internal services.
2. **Rate Limiting & Throttling:** Prevents DDoS and brute-force abuse per API key or IP address.
3. **SSL/TLS Termination:** Offloads HTTPS decryption at the perimeter.
4. **Load Balancing & Service Discovery:** Dynamically routes traffic across scaling instance replicas.

---

## How to Run & Verify

1. **Execute Pytest Test Suite**:
   ```bash
   pytest test_microservices.py -v
   ```

2. **Start Microservices Independently**:
   ```bash
   # Terminal 1: Course Service (Port 5001)
   python course_service/app.py

   # Terminal 2: Student Service (Port 5002)
   python student_service/app.py

   # Terminal 3: API Gateway (Port 5000)
   python gateway/app.py
   ```

3. **Verify End-to-End Gateway Routing**:
   ```bash
   # Enroll student through API Gateway
   curl -X POST http://localhost:5000/api/students/1/enroll \
        -H "Content-Type: application/json" \
        -d '{"course_id": 101}'
   ```
