# Dummy Error App

A Flask-based web application intentionally designed with specific bugs to demonstrate AutoSRE system capabilities. This application serves as a controlled testing environment where errors can be reliably triggered, logged, and analyzed.

## Features

- Flask web server with multiple endpoints (health check, authentication, data retrieval)
- Intentionally buggy service modules for testing error detection
- Automated error triggering script for simulating production traffic
- Real-time error reporting to AutoSRE incident API

## Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 (web framework)
- requests 2.31.0 (HTTP client for trigger script)

## Usage

### Running the Flask Application

Start the Flask server on port 8080:

```bash
python app.py
```

The application will start and display available endpoints:
- `GET /health` - Health check endpoint
- `POST /auth/login` - Authentication endpoint (triggers TypeError bug)
- `GET /api/data` - Data retrieval endpoint (triggers connection leak bug)

The server will continue running even after errors occur, allowing multiple error scenarios to be tested.

### Triggering Intentional Errors

In a separate terminal, run the error trigger script:

```bash
python trigger_errors.py
```

This script simulates production traffic by continuously sending requests to the Flask application. Press `Ctrl+C` to stop the simulation.

## Expected Error Behaviors

The application contains two intentional bugs for demonstration purposes:

### 1. Authentication TypeError

**Trigger:** POST request to `/auth/login` without an Authorization header

**Expected Behavior:**
- A `TypeError` is raised in `auth_service.py` (lines 15-20)
- Error occurs due to missing null check on the Authorization header
- Error message contains "NoneType"
- Error is logged to console and sent to the incident API

**When it occurs:** Immediately after the first authentication request from the trigger script

### 2. Database Connection Pool Exhaustion

**Trigger:** Multiple rapid GET requests to `/api/data`

**Expected Behavior:**
- Database connections are opened but not properly closed (missing finally block)
- Connection pool (max 5 connections) becomes exhausted
- A `ConnectionPoolExhausted` error is raised after 5-10 requests
- Error is logged to console and sent to the incident API

**When it occurs:** After 5-10 data requests from the trigger script

## Integration with AutoSRE

### Incident API

The application integrates with the AutoSRE incident API to report errors in real-time:

- **Endpoint:** `http://localhost:5000/incidents`
- **Method:** POST
- **Format:** JSON

Each error is automatically reported with the following information:
- Error type (e.g., TypeError, ConnectionPoolExhausted)
- Error message
- Source file name and line number
- Full stack trace
- Timestamp (ISO 8601 format)
- API endpoint that triggered the error

### Real-Time Monitoring

When the trigger script runs, the AutoSRE dashboard displays incidents in real-time, allowing you to:
- Monitor error patterns and frequency
- Analyze stack traces and error context
- Verify error detection capabilities
- Test incident response workflows

### Prerequisites for Integration

Ensure the AutoSRE incident API is running and accessible at `localhost:5000` before starting the Flask application and trigger script.

## Project Structure

```
dummy-error-app/
├── app.py                 # Main Flask application
├── auth_service.py        # Authentication service (contains TypeError bug)
├── db_connection.py       # Database connection module (contains leak bug)
├── error_logger.py        # Error logging and incident reporting
├── trigger_errors.py      # Automated error triggering script
├── requirements.txt       # Python dependencies
├── .gitignore            # Git exclusions
└── README.md             # This file
```

## Notes

- The bugs are **intentional** and should NOT be fixed - they are designed for AutoSRE testing
- The application continues running after errors occur to allow multiple error scenarios
- All errors are logged to both console and the incident API for comprehensive monitoring