# Page Pulse

Production-grade URL audit service built for the Digital Heroes Software Development task.

Page Pulse allows users to audit a URL and receive information about its HTTP status, response time, and whether the result was served from cache.

## Live Application

Live URL: `YOUR_DEPLOYED_URL`

API Documentation: `YOUR_DEPLOYED_URL/docs`

## Features

* URL input validation
* HTTP status auditing
* Response-time measurement
* Configurable request timeouts
* Concurrency limiting
* TTL-based caching
* Configurable cache duration
* Per-client rate limiting
* Structured error responses
* Unique request IDs
* Structured JSON logging
* Automated test suite
* Code quality checks with Ruff and Black
* GitHub Actions CI on every push and pull request
* Live deployment

## Architecture

```text
Client
  |
  v
POST /audit
  |
  v
Request ID Middleware
  |
  v
Rate Limiting
  |
  v
Cache Lookup
  |
  +---- Cache Hit ----> Return Cached Result
  |
  +---- Cache Miss
          |
          v
    Concurrency Limit
          |
          v
    URL Audit Service
          |
          v
    HTTP Request with Timeout
          |
          v
    Store Result in Cache
          |
          v
      Return Result
```

## Technology Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Programming language            |
| FastAPI           | API framework                   |
| Uvicorn           | ASGI server                     |
| HTTPX             | Asynchronous HTTP client        |
| Pydantic          | Request and response validation |
| Pydantic Settings | Environment configuration       |
| Pytest            | Testing                         |
| Pytest-Asyncio    | Async test support              |
| Pytest-Cov        | Test coverage                   |
| Ruff              | Linting                         |
| Black             | Code formatting                 |
| GitHub Actions    | Continuous Integration          |

All technologies used in this project are free and open source.

## Project Structure

```text
page-pulse/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_id.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── audit_schema.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── audit_service.py
│       ├── cache_service.py
│       └── rate_limit_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_audit.py
│   ├── test_cache.py
│   ├── test_errors.py
│   ├── test_health.py
│   └── test_rate_limit.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

## API Contract

### Health Check

```http
GET /
```

Returns the service landing page and confirms that Page Pulse is running.

The landing page includes the required footer credit:

**Built for Digital Heroes Training Task**

### Audit URL

```http
POST /audit
```

#### Request

```json
{
  "url": "https://example.com"
}
```

#### Successful Response

```json
{
  "request_id": "a7f4e1c2-1234-4567-8901-abcdef123456",
  "url": "https://example.com",
  "status_code": 200,
  "response_time_ms": 245.31,
  "is_cached": false
}
```

#### Cached Response

```json
{
  "request_id": "b8f5e2d3-2345-5678-9012-bcdefa234567",
  "url": "https://example.com",
  "status_code": 200,
  "response_time_ms": 245.31,
  "is_cached": true
}
```

## Error Responses

### Invalid URL

```http
422 Unprocessable Entity
```

### Rate Limit Exceeded

```http
429 Too Many Requests
```

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "request_id": "request-id"
  }
}
```

### Target URL Timeout

```http
504 Gateway Timeout
```

```json
{
  "error": {
    "code": "AUDIT_TIMEOUT",
    "message": "The target URL timed out",
    "request_id": "request-id"
  }
}
```

### Target URL Connection Failure

```http
502 Bad Gateway
```

```json
{
  "error": {
    "code": "AUDIT_CONNECTION_ERROR",
    "message": "Unable to connect to the target URL",
    "request_id": "request-id"
  }
}
```

## Configuration

Configuration is managed through environment variables.

Create a `.env` file based on `.env.example`:

```env
APP_NAME=Page Pulse
ENVIRONMENT=development
REQUEST_TIMEOUT_SECONDS=10
CACHE_TTL_SECONDS=300
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
MAX_CONCURRENT_REQUESTS=10
```

### Configuration Details

| Variable                    | Description                           | Default |
| --------------------------- | ------------------------------------- | ------- |
| `REQUEST_TIMEOUT_SECONDS`   | Maximum time to wait for a target URL | `10`    |
| `CACHE_TTL_SECONDS`         | How long audit results remain cached  | `300`   |
| `RATE_LIMIT_REQUESTS`       | Maximum requests per client           | `10`    |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate limit time window                | `60`    |
| `MAX_CONCURRENT_REQUESTS`   | Maximum simultaneous audits           | `10`    |

## Caching Design

Page Pulse uses an in-memory TTL cache.

When a URL is audited:

```text
First Request
     |
     v
Fetch URL
     |
     v
Store Result in Cache
```

A repeated request during the cache window:

```text
Request
   |
   v
Cache Hit
   |
   v
Return Cached Result
```

The cache duration is configurable using:

```env
CACHE_TTL_SECONDS=300
```

### Design Decision

The in-memory cache keeps the service dependency-free and simple to deploy.

For a multi-instance production deployment, a shared cache such as Redis would be more appropriate because each application instance would need access to the same cache. For this task, the in-memory approach is intentional and suitable for a single-instance deployment.

## Rate Limiting Design

Rate limiting is applied per client.

Example:

```text
Client A
  |
  +-- Request 1
  +-- Request 2
  +-- ...
  +-- Request 10
  |
  +-- Request 11 → Rejected
```

The rate limit is configurable:

```env
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
```

Different clients are tracked independently.

## Concurrency Control

The service uses a concurrency limit to prevent too many URL audits from running simultaneously.

Example:

```text
100 incoming requests
        |
        v
10 audits running
        |
        v
Remaining requests wait
```

This prevents excessive outbound requests and protects application resources.

## Request IDs

Every request receives a unique request ID.

Example:

```text
Request
   |
   v
request_id: abc-123
```

The request ID is:

* Included in successful responses
* Included in error responses
* Returned in the `X-Request-ID` response header
* Used for tracing structured logs

## Structured Logging

Application events are logged in structured JSON format.

Example:

```json
{
  "timestamp": "2026-07-25T10:30:00+00:00",
  "level": "INFO",
  "message": "audit_completed",
  "request_id": "abc-123",
  "url": "https://example.com"
}
```

Structured logs make it easier to search, filter, and troubleshoot application behaviour.

## Testing

The test suite covers important application behaviour, including:

* Health check
* Valid URL auditing
* Invalid URL validation
* Missing required fields
* Timeout handling
* Connection error handling
* Cache hits
* Cache expiration
* Rate limit enforcement
* Per-client rate limiting
* Request ID generation

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Code Quality

Run Ruff:

```bash
ruff check .
```

Run Black:

```bash
black .
```

Check Black formatting without modifying files:

```bash
black --check .
```

## Continuous Integration

GitHub Actions runs automatically on:

* Every push
* Every pull request

The CI pipeline:

```text
Push / Pull Request
        |
        v
Install Python
        |
        v
Install Dependencies
        |
        v
Run Ruff
        |
        v
Check Black Formatting
        |
        v
Run Pytest
```

A change is considered ready only when the CI checks pass.

## Running Locally

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd page-pulse
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update values if required.

### 5. Start the Application

```bash
uvicorn app.main:app --reload
```

### 6. Open the API Documentation

```text
http://127.0.0.1:8000/docs
```

## AI Usage

AI tools were used during development to help refine the requirements, explore the architecture, review implementation approaches, identify edge cases, improve error-handling strategies, and assist with test planning. The final implementation decisions, code integration, testing, debugging, and project structure were reviewed and adapted for this project.

## Footer Credit

The public landing page includes the required visible credit:

**Built for Digital Heroes Training Task**

The credit links to the Digital Heroes website as required by the task brief.

## Submission Checklist

* [ ] Public GitHub repository
* [ ] Complete source code
* [ ] Meaningful test suite
* [ ] CI configured
* [ ] CI runs on every push
* [ ] README includes API contract
* [ ] Application deployed live
* [ ] Live URL tested
* [ ] Required footer credit visible
* [ ] Footer credit links to `digitalheroesco.com`
* [ ] AI usage paragraph included
* [ ] Live URL included in submission

## License

This project was created as part of the Digital Heroes Software Development training task.
