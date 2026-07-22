# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

**Author:** Gopika R  
**Track:** Digital Nurture 5.0 - Python Full Stack Engineer Track  
**Module:** QA Concepts & Test Automation — Selenium Basics  

---

## Task 1: V-Model Mapping

### 9. Comprehensive V-Model Diagram

```
===================================================================================
                                      V-MODEL
===================================================================================

[ DEVELOPMENT LIFECYCLE (SDLC) ]                 [ TESTING LIFECYCLE (TDLC) ]
(Verification / Left Side)                       (Validation / Right Side)

1. Requirements Analysis  <=========================>  8. User Acceptance Testing
   (Business & User Specs)    [Acceptance Test Plan]     (UAT / Alpha & Beta)
         |                                                      ^
         v                                                      |
2. System Design Specification <====================>  7. System Testing
   (Functional Specifications)   [System Test Plan]       (E2E Functional & Non-Func)
         |                                                      ^
         v                                                      |
3. Architecture Design     <=========================>  6. Integration Testing
   (High Level Specs)           [Integration Test Plan]   (API / Database / Services)
         |                                                      ^
         v                                                      |
4. Module / Detailed Design <========================>  5. Unit Testing
   (Low Level Design)           [Unit Test Cases]         (Function / Class Level)
         \                                                      /
          \                                                    /
           \                                                  /
            +------------------> CODING <--------------------+
                              (Bottom Vertex)
===================================================================================
```

---

### 10. Test Artifacts Produced Per SDLC Phase

| SDLC Phase (Development) | Corresponding TDLC Phase (Testing) | Test Artifact Produced During Development Phase |
| :--- | :--- | :--- |
| **1. Requirements Analysis** | **User Acceptance Testing (UAT)** | **Acceptance Test Plan & UAT Test Scenarios**<br>Defines business acceptance criteria, user personas, and real-world college administrative workflows. |
| **2. System Design Specification** | **System Testing** | **System Test Plan & Functional Requirement Matrix**<br>Defines end-to-end system test suites, security test plans, and performance benchmark goals. |
| **3. Architecture Design** | **Integration Testing** | **Integration Test Plan & API Interface Test Specifications**<br>Defines interface stubs/mocks, API endpoint request/response schemas, and DB integration strategies. |
| **4. Module / Low Level Design** | **Unit Testing** | **Unit Test Suite & Code Coverage Goals**<br>Defines function-level test cases, boundary value inputs, and mock parameters for methods. |
| **5. Coding / Implementation** | **Test Execution** | **Executable Source Code & Developer Self-Test Execution Logs** |

---

### 11. Entry & Exit Criteria for Testing Levels

```
                          [ TESTING QUALITY GATES ]
      +---------------------------------------------------------------+
      |  ENTRY CRITERIA ---> [ TESTING LEVEL ] ---> EXIT CRITERIA     |
      +---------------------------------------------------------------+
```

#### A. Unit Testing
- **Entry Criteria:**
  1. Source code module compiles without syntax or build errors.
  2. Code peer-review completed and approved in pull request.
  3. Unit test framework and mock objects configured.
- **Exit Criteria:**
  1. 100% of planned unit tests executed with 100% pass rate.
  2. Minimum $85\%$ branch and line code coverage achieved.
  3. Zero unresolved critical static analysis issues (e.g., SonarQube/Pylint).

#### B. Integration Testing
- **Entry Criteria:**
  1. All component unit tests passed cleanly.
  2. API endpoints and database migration scripts deployed to Staging.
  3. Interface contract definitions (OpenAPI/Swagger) finalized.
- **Exit Criteria:**
  1. All inter-component data flows and API request/response integrations verified.
  2. Zero Critical or High severity defect tickets open.
  3. Integration test report generated and signed off.

#### C. System Testing
- **Entry Criteria:**
  1. Integration testing completed with sign-off.
  2. Complete system environment (Frontend + API Gateway + DB + Auth) deployed.
  3. Test data seeded in staging environment.
- **Exit Criteria:**
  1. 100% of end-to-end system test cases executed.
  2. Zero Critical (P1) or High (P2) severity bugs open.
  3. System response time and load benchmarks met.

#### D. User Acceptance Testing (UAT)
- **Entry Criteria:**
  1. System testing successfully completed and signed off by QA Lead.
  2. User documentation and release notes generated.
  3. UAT environment configured with production-like anonymized data.
- **Exit Criteria:**
  1. Business stakeholders / College Admins complete user scenario scripts.
  2. 100% of high-priority business acceptance criteria met.
  3. Formal UAT sign-off received from Product Owner.

---

### 12. Early QA Engagement Points in the V-Model

1. **Requirements Analysis Phase (Left-Hand Top of V-Model):**
   - **Engagement:** QA actively participates in static testing of user stories and Functional Requirement Specifications (FRS).
   - **Benefit:** Identifying ambiguous, incomplete, or untestable requirements (e.g., "the course search must be fast") *before* code is written prevents costly rework down the line.

2. **Architecture & API Design Phase (Left-Hand Middle of V-Model):**
   - **Engagement:** QA reviews API interface schemas (OpenAPI/Swagger definitions) and database entity-relationship models alongside system architects.
   - **Benefit:** QA can define contract test stubs early and ensure error payload formats, status codes, and authorization rules are consistently designed across all microservices.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Problems Caused by Traditional Waterfall Testing

In the Course Management API project, relying on traditional Waterfall testing (testing only after code completion) causes three major bottlenecks:

1. **Defect Multiplication & High Cost of Change:**
   - *Problem:* Requirements flaws or architectural design errors discovered during final system testing require tearing down database schemas and rewriting multiple controller layers.
   - *Impact:* Fixing a bug in system testing costs up to 10x-50x more than catching it during initial design.

2. **Testing Time Squeeze & Delayed Releases:**
   - *Problem:* Development delays eat into the scheduled testing window. QA is forced to rush test execution or compromise on test coverage to meet fixed release deadlines.
   - *Impact:* Critical bugs slip into production releases.

3. **Lack of Feedback Loop for Developers:**
   - *Problem:* Developers receive bug reports weeks after writing the original code, forcing them to re-contextualize forgotten logic.
   - *Impact:* Slow bug resolution cycles and reduced team velocity.

---

### 14. QA Engineer Role Across Agile Ceremonies

```
+-----------------------------------------------------------------------------+
|                         AGILE CEREMONY QA ROLES                             |
+-----------------------------------------------------------------------------+
| 1. Sprint Planning   ==> Define Acceptance Criteria & Gherkin Scenarios    |
| 2. Daily Standup     ==> Report Blockers, Environment & Test Status         |
| 3. Sprint Review     ==> Present Demo Testing & Feature Validation           |
| 4. Retrospective     ==> Drive Quality Process Improvements & Automation     |
+-----------------------------------------------------------------------------+
```

1. **Sprint Planning:**
   - QA collaborates with Product Owners and developers to refine user stories, estimate testing effort (story points), enforce the *Definition of Ready (DoR)*, and write Given-When-Then acceptance criteria.

2. **Daily Standup:**
   - QA reports daily progress on test case creation/execution, flags environment or test data blockers, and aligns with developers on fixed bug re-testing.

3. **Sprint Review (Demo):**
   - QA demonstrates validated features from an end-user perspective, highlights edge-case behaviors verified during the sprint, and provides immediate quality metric feedback.

4. **Retrospective:**
   - QA reviews sprint defect trends, identifies root causes of leaked defects, evaluates test automation coverage, and proposes concrete process improvements for the next sprint.

---

### 15. Concrete Shift-Left Practices for Course Management API

Shift-Left moves testing activities to earlier stages in the software lifecycle:

#### (a) Reviewing Requirements for Testability
- **Practice:** QA audits the requirement: *"Course codes must be formatted properly."*
- **Shift-Left Action:** QA refines this into testable rules: *"Course codes must consist of 2-4 uppercase alphanumeric characters followed by a hyphen and 3 digits (e.g., CS-101). Rejection must return 400 Bad Request."*

#### (b) Writing Test Cases Before Code (TDD / BDD)
- **Practice:** Behavioral-Driven Development (BDD).
- **Shift-Left Action:** QA and developers write executable Gherkin feature files *before* implementing the `POST /api/courses/` endpoint. Developers run tests locally while coding until all scenarios pass (Green).

#### (c) Static Code Analysis
- **Practice:** Automated linting and security scanning integrated into pre-commit hooks and CI pipelines.
- **Shift-Left Action:** Tools like `flake8`, `bandit`, and `SonarQube` check Python code for type mismatches, SQL injection vulnerabilities, and unused variables on every developer commit before merging.

#### (d) API Contract Testing Before Integration
- **Practice:** Consumer-Driven Contract Testing using tools like Pact.
- **Shift-Left Action:** QA defines JSON contract schemas for `/api/courses/` payloads. Frontend and backend teams test independently against mock servers matching the contract before full system integration.

---

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:**  
*As a college admin, I want to create a new course, so that students can enroll in it.*

#### Scenario 1: Happy Path - Successfully create a new course
```gherkin
Feature: Create Course API
  As a college admin
  I want to create a new course
  So that students can enroll in it

  Scenario: Create a valid new course with all required fields
    Given the college admin is authenticated with a valid JWT token
    And a course with code "CS-201" does not exist in the catalog
    When the admin sends a POST request to "/api/courses/" with the following body:
      """
      {
        "code": "CS-201",
        "name": "Data Structures & Algorithms",
        "credits": 4,
        "department": "Computer Science"
      }
      """
    Then the response status code should be 201
    And the response header "Content-Type" should be "application/json"
    And the response body should contain a generated "id"
    And the response body field "code" should equal "CS-201"
    And the course "CS-201" should be present in the database catalog
```

#### Scenario 2: Negative Path - Duplicate course code rejection
```gherkin
  Scenario: Reject creation of a course with an existing course code
    Given the college admin is authenticated with a valid JWT token
    And a course with code "CS-201" already exists in the catalog
    When the admin sends a POST request to "/api/courses/" with the following body:
      """
      {
        "code": "CS-201",
        "name": "Advanced Data Structures",
        "credits": 4,
        "department": "Computer Science"
      }
      """
    Then the response status code should be 409
    And the response body field "error" should equal "Conflict"
    And the response body field "message" should equal "Course code 'CS-201' already exists."
```

#### Scenario 3: Negative Path - Missing required mandatory fields
```gherkin
  Scenario: Reject creation when mandatory course name is missing
    Given the college admin is authenticated with a valid JWT token
    When the admin sends a POST request to "/api/courses/" with the following body:
      """
      {
        "code": "CS-202",
        "credits": 3,
        "department": "Computer Science"
      }
      """
    Then the response status code should be 400
    And the response body field "error" should equal "Bad Request"
    And the response body error list should contain "Field 'name' is required."
```
