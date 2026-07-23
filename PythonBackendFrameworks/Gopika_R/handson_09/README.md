# Hands-On 9: Authentication & Security — JWT, OAuth2 & OWASP

## Overview
This hands-on exercise implements a secure authentication system using **FastAPI**, **Passlib (bcrypt password hashing)**, **python-jose (JWT token generation & validation)**, **OAuth2 password bearer dependency**, and **CORS middleware**.

---

## Task 1: Password Hashing & User Registration

### 1. User Model & Schema
- **Model (`models.py`)**: `id` (int PK), `email` (unique index), `hashed_password` (str), `is_active` (bool).
- **Validation (`schemas.py`)**: `email` verified via Pydantic `EmailStr`.

### 2. Password Hashing Utility (`security.py`)
- Configured `passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")`.
- `get_password_hash(password: str)`: Hashes plain text using bcrypt scheme.
- `verify_password(plain_password, hashed_password)`: Verifies credentials securely.

### 3. Registration Endpoint (`POST /api/v1/auth/register/`)
- Checks if the requested email is already registered; if so, returns **`HTTP 409 Conflict`** with detail `"Email already registered"`.
- Hashes the plain password before database insertion. Plain-text passwords are **NEVER** stored or logged.

### 4. Rationale: Why bcrypt Over MD5 / SHA-256?
- **MD5 and SHA-256** are fast cryptographic hash algorithms optimized for high throughput. Their execution speed makes them vulnerable to GPU-accelerated dictionary attacks and pre-computed rainbow tables.
- **bcrypt** incorporates an adaptive work factor (cost parameter) and automatic unique salting. It intentionally introduces computational latency per hash evaluation, rendering brute-force attacks computationally infeasible.

---

## Task 2: JWT Login, Protected Routes & CORS Configuration

### 1. JWT Login Endpoint (`POST /api/v1/auth/login/`)
- Accepts user credentials, verifies using `verify_password()`.
- Generates a signed JWT access token using `python-jose` with an expiration duration of **30 minutes**.
- Returns `{"access_token": token, "token_type": "bearer"}`.

### 2. Protected Route Dependency (`get_current_user`)
- Decodes and validates JWT bearer tokens from incoming `Authorization: Bearer <token>` headers.
- Raises **`HTTP 401 Unauthorized`** if the token is invalid, tampered with, or expired.
- Applied to protected endpoints:
  - `POST /api/v1/courses/` (Protected — 401 without valid token)
  - `DELETE /api/v1/courses/{id}/` (Protected — 401 without valid token)
  - `GET /api/v1/courses/` (Public — Accessible unauthenticated)

### 3. CORS Configuration
- Middleware configured using `CORSMiddleware` to allow requests originating from `http://localhost:3000`.

### 4. Security Documentation & Concepts
- **OAuth2 Authorization Code Flow vs Simple JWT Login:**
  - *Simple JWT Login (Resource Owner Password Credentials):* Client submits raw username & password directly to the API in exchange for tokens. Suitable for first-party, highly-trusted clients.
  - *OAuth2 Authorization Code Flow:* User authenticates directly on a third-party Identity Provider (IdP like Google or GitHub). The IdP issues a temporary authorization code, which the client backend exchanges for access tokens out-of-band. The client application never handles or sees user passwords.
- **JWT Payload Warning:** Claims in a JWT are base64-encoded strings, **NOT ENCRYPTED**. Confidential data (passwords, credit card numbers, SSNs) must never be stored in JWT payloads.
- **CORS Mechanics:** CORS headers are sent by the server to instruct browser engines which cross-origin requests are permitted. CORS is browser-enforced and does not protect backend APIs against non-browser HTTP clients (e.g. curl, backend microservices).

---

## How to Run & Verify

1. **Run Pytest Test Suite**:
   ```bash
   pytest test_security_auth.py -v
   ```

2. **Run Server Directly**:
   ```bash
   uvicorn main:app --port 8000 --reload
   ```
