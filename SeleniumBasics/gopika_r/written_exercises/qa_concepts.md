# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

**Author:** Gopika R  
**Track:** Digital Nurture 5.0 - Python Full Stack Engineer Track  
**Module:** QA Concepts & Test Automation — Selenium Basics  

---

## Task 1: Map Testing Types to a Real System

### 1. Concrete Test Cases Across Testing Levels (Course Management API)

Below is one concrete test case for each level of testing applied to the **Course Management API**:

#### A. Unit Testing (Isolated Function Level)
- **Target Component:** `validate_course_code(code_string: str) -> bool` function in the validation module.
- **Description:** Test that the `validate_course_code` function returns `False` when passed a string with special characters (e.g., `"CS@101"`), without instantiating any database connection or network calls.
- **Scope:** Single function execution in complete isolation using unit test stubs/mocks.

#### B. Integration Testing (Component Interaction Level)
- **Target Components:** `POST /api/courses/` API router handler + PostgreSQL Database Layer (`CourseRepository`).
- **Description:** Verify that when a valid JSON payload is sent to `POST /api/courses/`, the handler correctly invokes the database service and commits a new record into the `courses` database table with the exact assigned `course_id`.
- **Scope:** Interaction between API endpoint layer and data access layer.

#### C. System Testing (End-to-End System Level)
- **Target System:** Full Course Management API System (API Gateway + Auth Service + Course Service + Database + Audit Logger).
- **Description:** Execute a complete workflow: Authenticate user, call `POST /api/courses/` to create a course, invoke `GET /api/courses/{id}` to verify data persistence, verify that an asynchronous notification event is published to RabbitMQ, and check that an audit record is created in the audit log table.
- **Scope:** Complete end-to-end software system testing across all integrated sub-systems and protocols.

#### D. User Acceptance Testing - UAT (Business/User Perspective)
- **Target Persona:** College Department Administrator.
- **Description:** A college admin logs into the Administrative Portal UI, accesses the Course Catalog management module, fills out the form to add a new elective course "CS-305: Cloud Computing Architecture", assigns Professor Vance as the instructor, sets a cap of 60 students, and publishes it so students can view and register for the course during open enrollment.
- **Scope:** Real-world business process validation ensuring the system meets business requirements and user expectations.

---

### 2. Functional vs Non-Functional Classification

| Test Case | Type | Classification | Justification |
| :--- | :--- | :--- | :--- |
| Unit Test: `validate_course_code()` | Unit | **Functional** | Verifies specific input/output logic behavior against functional specification. |
| Integration Test: Router + DB persistence | Integration | **Functional** | Verifies correct business data storage logic across components. |
| System Test: Full API lifecycle & auditing | System | **Functional** | Checks end-to-end execution of functional capabilities. |
| UAT: Admin portal course setup | UAT | **Functional** | Validates user workflow against business requirements. |

#### Non-Functional Test Example (Performance & Load Testing)
- **Scenario:** **Load & Response Time Testing on `GET /api/courses/` Endpoint**
- **Description:** Simulate 200 concurrent user requests per second (RPS) hitting the `GET /api/courses/` endpoint over a 15-minute duration.
- **Pass Criteria:**
  - 95th percentile response time (P95) must be <= 150 ms.
  - System CPU utilization must remain below 75%.
  - Error rate must be 0.00%.
- **Focus:** Evaluates *how well* the system performs under load rather than *what* functions it performs.

---

### 3. Black-Box Testing vs White-Box Testing

```
+-----------------------------------------------------------------------+
|                         BLACK-BOX TESTING                             |
|  Inputs  ================> [ System Under Test ] ===============> Outputs |
|                            (Internal Code Hidden)                     |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                         WHITE-BOX TESTING                             |
|  Inputs  ===> [ Code Paths | Branching | Memory | DB Queries ] ===> Outputs|
|               (Internal Logic Fully Visible & Analyzed)               |
+-----------------------------------------------------------------------+
```

| Dimension | Black-Box Testing | White-Box Testing |
| :--- | :--- | :--- |
| **Knowledge of Code** | Requires NO knowledge of internal source code, structure, or implementation. | Requires full access and understanding of source code, algorithms, and architecture. |
| **Testing Focus** | System requirements, functional specs, user workflows, input/output validation. | Code coverage, branch coverage, path analysis, exception handling, data structures. |
| **Primary Operator** | **QA Engineers / Testers**, Business Analysts, End-Users (UAT). | **Software Developers**, Security Engineers, Code Reviewers. |
| **Techniques Used** | Equivalence Partitioning, Boundary Value Analysis, Decision Tables, Use Cases. | Statement Coverage, Branch Coverage, Path Testing, Mutation Testing. |

---

### 4. Formal Test Cases for `POST /api/courses/` Endpoint

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_API_001** | Verify successful creation of a new course with valid payload (Happy Path) | Admin user authenticated; JWT token available; Course code `CS101` does not exist in DB. | 1. Send `POST /api/courses/` with headers `Authorization: Bearer <valid_token>` and body: `{"code": "CS101", "name": "Intro to Computer Science", "credits": 3, "department": "CS"}`.<br>2. Inspect HTTP response status code and JSON body. | Status Code: `201 Created`. Response body contains created course object with generated `id` and matching `code`, `name`, `credits`, `department`. | | |
| **TC_API_002** | Verify system prevents creation of course with duplicate course code | Admin user authenticated; Course code `CS101` already exists in database. | 1. Send `POST /api/courses/` with header `Authorization: Bearer <valid_token>` and body containing duplicate `code`: `"CS101"`. | Status Code: `409 Conflict` or `400 Bad Request`. JSON error body contains message: `"Course code CS101 already exists."` | | |
| **TC_API_003** | Verify API validation failure when mandatory fields are missing | Admin user authenticated. | 1. Send `POST /api/courses/` with body missing the required `name` field: `{"code": "CS102", "credits": 4}`. | Status Code: `400 Bad Request` or `422 Unprocessable Entity`. Response contains validation error message indicating `name` is a required field. | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle (State Transition Workflow)

```
        +---------+
        |   NEW   |
        +----+----+
             |
             v
       +-----------+
       | ASSIGNED  |
       +-----+-----+
             |
             v
        +----------+           +------------+
        |   OPEN   | --------> |  REJECTED  | (Invalid/Not a Bug)
        +----+-----+           +------------+
             |                       |
             |                       v
             |                 +------------+
             |                 |   CLOSED   |
             |                 +------------+
             v
        +----------+           +------------+
        |  FIXED   | --------> |  DEFERRED  | (Postponed to future release)
        +----+-----+           +------------+
             |
             v
        +----------+
        |  RETEST  |
        +----+-----+
             |
       +-----+-----+
       |           |
       v           v
+----------+   +----------+
| VERIFIED |   |  REOPEN  | (Bug still exists)
+----+-----+   +----+-----+
     |              |
     v              +-----> Returns to OPEN
+----------+
|  CLOSED  |
+----------+
```

#### Defect States & Transitions:
- **NEW:** Defect reported by QA for the first time.
- **ASSIGNED:** Defect acknowledged and assigned to a developer for triage/resolution.
- **OPEN:** Developer is actively analyzing and fixing the issue.
- **FIXED:** Developer has checked in the fix and deployed to the test environment.
- **RETEST:** QA picks up the fixed build to run test cases.
- **VERIFIED:** QA confirms the bug is fixed and system behaves as expected.
- **CLOSED:** QA closes the defect ticket permanently.
- **REOPEN:** If the fix fails retesting, the ticket is transitioned back to OPEN with updated logs.
- **REJECTED Path:** The developer or lead determines the bug is duplicate, invalid, or working as designed; ticket is closed with justification.
- **DEFERRED Path:** The bug is recognized as valid but low priority/impact, so resolution is scheduled for a future sprint/release.

---

### 6. Severity & Priority Classification Matrix

| Bug Scenario | Severity | Priority | Technical Justification |
| :--- | :--- | :--- | :--- |
| **a) `POST /api/courses/` returns 500 Internal Server Error for all requests.** | **Critical** | **P1 (Immediate)** | **Severity:** Core feature is completely unusable for all users with no workaround.<br>**Priority:** Blocks all course creation and downstream integrations; requires immediate hotfix. |
| **b) Course names longer than 150 characters are silently truncated without an error.** | **Medium** | **P2 (High)** | **Severity:** Data integrity issue; data is altered silently without system crash.<br>**Priority:** Must be addressed in current sprint to prevent database pollution and user confusion. |
| **c) The `/docs` Swagger page has a typo in the API description.** | **Low** | **P4 (Low)** | **Severity:** Minor cosmetic text issue with zero impact on API functionality or stability.<br>**Priority:** Low urgency; can be fixed during routine documentation cleanup. |
| **d) Login with correct credentials occasionally returns 401 on first attempt (intermittent).** | **High** | **P1 (Immediate)** | **Severity:** Impacts core authentication security and user trust.<br>**Priority:** Intermittent auth bugs often signal deep race conditions, cache synchronization failures, or memory leaks; must be prioritized immediately before release. |

---

### 7. Complete Formal Defect Report for Bug (a)

```
================================================================================
DEFECT REPORT
================================================================================
Defect ID      : DEF-2026-0101
Title          : POST /api/courses/ returns 500 Internal Server Error for all valid requests
Project        : Course Management System
Component      : Course API Service (`/api/courses/`)
Environment    : QA Staging Server (Ubuntu 22.04 LTS, Python 3.10, PostgreSQL 14)
Build Version  : v2.4.0-rc1
Reporter       : Gopika R (QA Engineer)
Assigned To    : Lead Backend Developer
Severity       : Critical
Priority       : P1 (Blocker)
Status         : NEW
Date Reported  : 2026-07-22

--------------------------------------------------------------------------------
SUMMARY:
When sending a valid POST request to `/api/courses/` to create a new course, 
the server fails with an HTTP 500 Internal Server Error instead of creating 
the course and returning 201 Created.

--------------------------------------------------------------------------------
PRECONDITIONS:
1. User possesses a valid Admin JWT authentication token.
2. The QA Staging environment API gateway and database services are running.

--------------------------------------------------------------------------------
STEPS TO REPRODUCE:
1. Open Postman or execute cURL command.
2. Prepare HTTP POST request to `https://staging-api.courseapp.com/api/courses/`.
3. Set Header: `Authorization: Bearer <valid_admin_jwt>`.
4. Set Header: `Content-Type: application/json`.
5. Provide valid JSON payload:
   {
     "code": "CS-401",
     "name": "Advanced Software Architecture",
     "credits": 4,
     "department": "Computer Science"
   }
6. Send the POST request.

--------------------------------------------------------------------------------
EXPECTED RESULT:
- Response HTTP Status: `201 Created`
- Response Payload contains created course object with generated UUID `id`.
- Record successfully persisted in PostgreSQL database `courses` table.

--------------------------------------------------------------------------------
ACTUAL RESULT:
- Response HTTP Status: `500 Internal Server Error`
- Response Payload:
  {
    "status": 500,
    "error": "InternalServerError",
    "message": "Unhandled NullReferenceException in CourseRepository.cs:line 42"
  }
- No record is created in the database.

--------------------------------------------------------------------------------
ATTACHMENTS:
1. screenshot_of_500_error.png (Capturing Postman 500 error response and headers)
2. server_application_log_DEF20260101.log (Contains full stack trace)
================================================================================
```

---

### 8. Severity vs. Priority Distinction

- **Severity:** Reflects the **technical impact** of the defect on the system architecture, data integrity, or core functionality. It is determined by QA based on technical criteria.
- **Priority:** Reflects the **business urgency** of fixing the defect. It is determined by Product Owners / Project Managers based on business timelines and release goals.

#### Real-World Example: High Severity but Low Priority
- **Scenario:** The legacy monthly data export module crashes with an unhandled exception (`Severity: High/Critical`) when processing records older than 10 years.
- **Why Low Priority (P4):** The annual audit export was completed yesterday, and this specific legacy export module will only be run again in 12 months. Additionally, the team is sunsetting this module next month in favor of a new analytics service. Therefore, while technical severity is high, fixing it has minimal immediate business urgency (**Low Priority**).

#### Real-World Example: Low Severity but High Priority
- **Scenario:** The company logo image on the login page of the public web application is displayed upside down or has a visible typo in the company tagline (`Severity: Low`).
- **Why High Priority (P1/P2):** The app is launching publicly today to major media outlets. While technical functionality is completely unaffected, the visual bug harms brand reputation and executive visibility (**High Priority**).
