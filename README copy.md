# GitHub Gists API Solution

A simple HTTP web server API that fetches and displays publicly available GitHub Gists for any user.

## Overview

This solution provides:
- HTTP API endpoint `/<username>` that returns a user's public gists
- Automated tests with mocking and integration testing
- Docker containerization listening on port 8080
- Clean, simple implementation in Python using Flask

## Prerequisites

- Python 3.9 or higher
- Docker (for containerized deployment)
- pip (Python package manager)

## Setup and Run

### Option 1: Run Locally (with Virtual Environment)

**Quick Start:**
```bash
./setup.sh
```

The setup script will create a Python virtual environment, activate it, and install all dependencies.

**Manual Setup:**

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

4. The API will be available at `http://localhost:8080`

5. When finished, deactivate the virtual environment:
```bash
deactivate
```

### Option 2: Run with Docker

1. Build the Docker image:
```bash
docker build -t github-gists-api .
```

2. Run the basic Docker SAST and resolve any issues from the recommendations:
```bash
docker scout quickview
docker scout recommendations local://github-gists-api:latest
```

3. Run the container as the non-root user:
```bash
docker run -p 8080:8080 --user mike --name gistapi -d github-gists-api
```

4. The API will be available at `http://localhost:8080`

## Usage

### Fetch User Gists

Make a GET request to `/<username>`:

```bash
curl http://localhost:8080/octocat
```

Example response:
```json
{
  "username": "octocat",
  "gist_count": 8,
  "gists": [
    {
      "id": "abc123",
      "description": "Example gist",
      "public": true,
      "html_url": "https://gist.github.com/octocat/abc123",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z",
      "files": ["example.txt"]
    }
    // ... more gists ...
  ]
}
```

### Health Check

```bash
curl http://localhost:8080/
```

Response:
```json
{
  "status": "healthy",
  "message": "GitHub Gists API is running. Use /<username> to fetch gists."
}
```

## Running Tests

Make sure your virtual environment is activated first:

```bash
source venv/bin/activate
```

Then execute the automated test suite:

```bash
pytest test_app.py -v
```

The test suite includes:
- Unit tests with mocked GitHub API responses
- Error handling tests (user not found, network errors)
- Integration test with the real GitHub API using the `octocat` user

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check endpoint |
| `/<username>` | GET | Fetch public gists for the specified GitHub user |

## Error Handling

- `404`: User not found on GitHub
- `500`: Server error (network issues, GitHub API problems)

## Technical Details

### Technology Stack
- **Language**: Python 3.12
- **Web Framework**: Flask 3.1.0
- **HTTP Client**: requests 2.32.3
- **Testing**: pytest 8.3.4 with pytest-mock 3.14.0

### Design Decisions

1. **Simple and Clear**: Used Flask for its simplicity and minimal boilerplate
2. **Virtual Environment**: Isolated Python dependencies to avoid conflicts with system packages
3. **Error Handling**: Proper HTTP status codes and error messages
4. **Type Hints**: Added type annotations for better code clarity
5. **Testing Strategy**: Mix of unit tests (with mocks) and integration tests
6. **Docker Security**: Container runs as non-root user (appuser) for better security
7. **Docker Simplicity**: Multi-stage build not needed for this simple app; kept Dockerfile minimal
8. **No Authentication**: GitHub API allows unauthenticated requests with reasonable rate limits

### Project Structure

```
.
├── app.py              # Main application code
├── test_app.py         # Automated tests
├── requirements.txt    # Python dependencies
├── setup.sh            # Virtual environment setup script
├── Dockerfile          # Docker container configuration
├── .dockerignore       # Files to exclude from Docker image
├── .gitignore          # Git ignore patterns
└── SOLUTION.md         # This file
```

## Potential Enhancements

The following features could be added but are not implemented to keep the solution simple:
- **TLS**: Add simple TLS support for secure inbound connections
- **Pagination**: Handle users with many gists
- **Caching**: Cache GitHub API responses to reduce API calls
- **Rate Limiting**: Protect against abuse
- **GitHub Token**: Support GitHub token for higher rate limits
- **Rewrite as a monolith**: Port this to a language like Golang.  Run it as a single binary without dependencies for simplicity, size and speed.
