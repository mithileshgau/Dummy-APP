# Implementation Plan: Dummy Error App

## Overview

This plan implements a Flask application with intentional bugs for AutoSRE demonstration. The implementation follows a bottom-up approach: first creating the buggy service modules, then the Flask application that uses them, then the error logging infrastructure, and finally the traffic simulation script.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create project root directory structure
  - Create requirements.txt with Flask and requests dependencies
  - Create .gitignore with Python standard exclusions (\_\_pycache\_\_, *.pyc, .env, venv/)
  - _Requirements: 6.1, 6.4, 6.5_

- [x] 2. Implement buggy authentication service
  - [x] 2.1 Create auth_service.py with intentional null pointer bug
    - Implement validate_auth function that accesses Authorization header without null check
    - Ensure bug is located between lines 15-20
    - Function should attempt to call .split() or similar on None value
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 3. Implement buggy database connection module
  - [x] 3.1 Create db_connection.py with intentional connection leak
    - Implement connection pool with max 5 connections
    - Implement get_connection function that opens connections without finally block
    - Implement query_data function that uses connections
    - Ensure connections are not properly closed after use
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Implement error logging infrastructure
  - [x] 4.1 Create error logger module
    - Implement log_error function that logs to console with timestamp
    - Implement send_to_incident_api function that POSTs to localhost:5000/incidents
    - Extract error type, message, file, line number, and stack trace from exceptions
    - Format incident data as JSON with all required fields
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 8.1, 8.2_

- [x] 5. Implement Flask application with endpoints
  - [x] 5.1 Create app.py with Flask server
    - Initialize Flask app on port 8080
    - Implement GET /health endpoint returning {"status": "healthy"}
    - Implement POST /auth/login endpoint that calls auth_service.validate_auth
    - Implement GET /api/data endpoint that calls db_connection.query_data
    - Add error handling middleware that catches exceptions and calls error logger
    - Add startup logging message
    - Ensure app continues running after errors occur
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.5, 8.4_

- [x] 6. Checkpoint - Test Flask application manually
  - Ensure Flask app starts on port 8080
  - Ensure /health endpoint returns 200 OK
  - Ask the user if questions arise

- [x] 7. Implement error trigger script
  - [x] 7.1 Create trigger_errors.py script
    - Implement trigger_auth_bug function that POSTs to /auth/login without Authorization header
    - Implement trigger_db_bug function that sends 10+ rapid GET requests to /api/data
    - Implement run_traffic_simulation function with continuous loop
    - Add delays between requests to simulate realistic traffic
    - Make script executable as standalone Python script
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 8. Create project documentation
  - [x] 8.1 Create README.md with setup and usage instructions
    - Document how to install dependencies (pip install -r requirements.txt)
    - Document how to run Flask app (python app.py)
    - Document how to run trigger script (python trigger_errors.py)
    - Document expected error behaviors (TypeError after auth request, ConnectionPoolExhausted after 5-10 data requests)
    - Document integration with AutoSRE incident API
    - _Requirements: 6.6, 7.3, 7.4, 7.5, 8.3_

- [x] 9. Initialize git repository and create commits
  - [x] 9.1 Initialize git repository and commit project files
    - Run git init
    - Create initial commit with project structure
    - Create commit for each major component (auth service, db connection, Flask app, trigger script)
    - Use meaningful commit messages describing each component
    - _Requirements: 7.1, 7.2_

- [-] 10. Final checkpoint - Verify end-to-end functionality
  - Ensure Flask app runs without startup errors
  - Ensure trigger script successfully triggers both bugs
  - Ensure errors are logged to console
  - Ask the user to verify incident API receives error reports
  - _Requirements: 8.5_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- The bugs are intentional and should NOT be fixed
- The application should continue running after errors occur to allow multiple error scenarios
- Ensure the incident API endpoint (localhost:5000/incidents) is available before testing integration
