"""
Django Web Framework Foundations & Architecture Notes
=====================================================

1. Request-Response Lifecycle for GET /api/courses/
-----------------------------------------------------
Journey of an HTTP GET request through a Django application:
Browser HTTP Request -> Web Server (e.g., Gunicorn/WSGI) -> Django Middleware Stack -> URL Router (urls.py) -> View Function/Class (views.py) -> Model Query / Database (models.py / ORM) -> View returns Response -> Middleware (Response Processing) -> Web Server -> Browser HTTP Response.

Step-by-step breakdown:
a. URL Router: Matches the request URL `/api/courses/` against registered patterns in `urls.py` and dispatches to the corresponding view.
b. View: Handles request logic, interacts with models, and prepares the HTTP response payload.
c. Model (DB Query): Performs database queries using Django ORM to retrieve or persist Course data.
d. Response: Constructs an `HttpResponse` or `JsonResponse` object containing data and HTTP status code.


2. Middleware in Django
-----------------------
Middleware is a framework of hooks into Django's request/response processing. It is a light, low-level 'plugin' system for globally altering Django’s input or output.

Where it sits: Sits between the request entering Django and reaching the URL router/view, and between the view returning a response and sending it back to the client.

Two Built-in Django Middleware Classes:
a. `django.middleware.security.SecurityMiddleware`:
   Provides several security enhancements to the request/response cycle, such as setting HTTP Strict Transport Security (HSTS) headers, X-Content-Type-Options, and SSL redirects.
b. `django.middleware.csrf.CsrfViewMiddleware`:
   Protects against Cross-Site Request Forgery (CSRF) attacks by ensuring incoming POST/PUT/DELETE requests have a valid CSRF token.


3. WSGI vs ASGI
---------------
- WSGI (Web Server Gateway Interface): Synchronous Python standard for web applications. Handles requests sequentially per worker process/thread.
- ASGI (Asynchronous Server Gateway Interface): Asynchronous standard extending WSGI to support async Python (`async`/`await`), WebSockets, HTTP/2, and long-lived connections.

Django Default:
Django uses WSGI by default (`wsgi.py`).

When to switch to ASGI:
Switch to ASGI (`asgi.py` with servers like Uvicorn or Daphne) when your project requires real-time capabilities (WebSockets via Django Channels), high-concurrency async HTTP requests, or async view handlers.


4. MVC vs Django's MVT Pattern
------------------------------
MVC (Model-View-Controller) vs MVT (Model-View-Template):

- M (Model) -> Model: Maps directly to Django Models (`models.py`). Handles data structures, database schema, and ORM operations.
- V (View)  -> Template: In MVT, the HTML/JSON presentation layer is called the 'Template' (or JSON response payload). It handles how data is displayed.
- C (Controller) -> View: In MVT, Django's 'View' (`views.py`) acts as the Controller. It receives HTTP requests, executes business logic, calls models, and returns responses.
"""
