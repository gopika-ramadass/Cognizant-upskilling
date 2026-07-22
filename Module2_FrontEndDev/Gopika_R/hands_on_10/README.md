# Hands-On 10: API Integration & Advanced State Management

## Overview
This hands-on exercise completes the Student Portal application by establishing a **Centralised API Service Layer**, implementing **Advanced Redux Toolkit State Management with Async Thunks**, adding **Global Error Boundaries**, and comparing state management architectures across modern frontend frameworks (React, Angular, Vue).

---

## Task 1: Centralised API Service Layer
- **Configured Axios Instance (`src/api/apiClient.ts`)**:
  - `baseURL`: `https://jsonplaceholder.typicode.com`
  - `timeout`: `5000ms`
  - `headers`: `Content-Type: application/json`
- **Request Interceptor**:
  - Automatically attaches a mock Authorization header (`Bearer mock-token-xyz`) to every outgoing request.
  - Logs outgoing API calls to the console (`[API Interceptor] API Request Started`).
- **Response Interceptor**:
  - Unwraps `response.data` so calling functions receive pure domain data directly.
  - Standardises API errors into a uniform `{ message, statusCode }` object.
- **Service Module (`src/api/courseApi.ts`)**:
  - Exports clean API functions (`getAllCourses()`, `getCourseById()`, `enrollStudent()`) consumed by Redux thunks.

---

## Task 2: Advanced Redux Toolkit (Async Thunks)
- **Async Thunk (`src/store/coursesSlice.ts`)**:
  - Implements `createAsyncThunk('courses/fetchAll', ...)` to encapsulate API data fetching.
- **Slice ExtraReducers**:
  - `pending`: Sets `loading = true` and clears previous errors.
  - `fulfilled`: Updates `courses` state with fetched catalog and sets `loading = false`.
  - `rejected`: Captures error payload, sets `error` message, and resets `loading = false`.
- **Selector Functions**:
  - `selectCourses`, `selectCoursesLoading`, `selectCoursesError` decouple components from the store's underlying shape.

---

## Task 3: State Management Comparison Across Frameworks

| Feature / Metric | React + Redux Toolkit (RTK) | Angular + NgRx | Vue 3 + Pinia |
| :--- | :--- | :--- | :--- |
| **Boilerplate Level** | **Low to Medium** (`createSlice`, `createAsyncThunk` eliminate legacy Redux boilerplate). | **High** (Requires Actions, Reducers, Effects, Selectors, and RxJS Observables). | **Minimal** (Setup Store syntax matches Composition API `ref()` & `computed()`). |
| **Async Side Effects** | `createAsyncThunk` or RTK Query. | NgRx Effects (`@Effect()`, RxJS `createEffect`). | Async functions directly inside store actions. |
| **Learning Curve** | **Moderate** (Requires understanding dispatch, actions, and immutability via Immer). | **Steep** (Requires strong mastery of RxJS streams, Observables, and Dependency Injection). | **Gentle / Low** (Very intuitive for standard Vue 3 developers). |
| **Built-in Tooling** | Redux DevTools Extension (Time-travel debugging, action logs, state diffs). | Redux DevTools Integration & Angular DevTools. | Vue DevTools Extension with native Pinia tab. |
| **TypeScript Support** | Native & seamless with type inference. | Strong & built-in by default. | Native & effortless with Composition API. |

---

## How to Run & Verify

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Run Development Server**:
   ```bash
   npm run dev
   ```

3. **Production Build**:
   ```bash
   npm run build
   ```

4. **Verify Features**:
   - Observe automatic course catalog loading via Axios & Async Thunk on mount.
   - Enroll / unenroll courses to verify Redux store state mutations.
   - Click **"🧪 Test Error Boundary Crash"** to trigger component exception and observe the global fallback UI.
