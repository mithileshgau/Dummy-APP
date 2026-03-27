"""
Error Logger Module

This module provides error logging and incident reporting functionality.
Logs errors to console and forwards them to the AutoSRE incident API.
"""

import traceback
import requests
from datetime import datetime
from typing import Optional


def log_error(error: Exception, context: Optional[dict] = None) -> None:
    """
    Logs error to console and sends to incident API.
    
    Args:
        error: The exception that occurred
        context: Additional context (endpoint, request info, etc.)
    """
    if context is None:
        context = {}
    
    # Extract error details from the exception
    error_type = type(error).__name__
    message = str(error)
    
    # Extract file, line number, and stack trace from traceback
    tb = traceback.extract_tb(error.__traceback__)
    stack_trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    
    # Get the last frame (where the error actually occurred)
    if tb:
        last_frame = tb[-1]
        file = last_frame.filename
        line = last_frame.lineno
    else:
        file = "unknown"
        line = 0
    
    # Get timestamp in ISO 8601 format
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Log to console with timestamp
    print(f"[{timestamp}] ERROR: {error_type}: {message}")
    print(f"  File: {file}, Line: {line}")
    print(f"  Stack trace:\n{stack_trace}")
    
    # Prepare incident data
    incident_data = {
        "error_type": error_type,
        "message": message,
        "file": file,
        "line": line,
        "stack_trace": stack_trace,
        "timestamp": timestamp,
        "endpoint": context.get("endpoint", "unknown")
    }
    
    # Send to incident API
    send_to_incident_api(incident_data)


def send_to_incident_api(incident_data: dict) -> None:
    """
    Sends incident report to the AutoSRE incident API.
    
    Args:
        incident_data: Dictionary containing error details
    """
    api_url = "http://localhost:5000/incidents"
    
    try:
        response = requests.post(api_url, json=incident_data, timeout=5)
        if response.status_code == 200:
            print(f"  Incident reported successfully to {api_url}")
        else:
            print(f"  Warning: Incident API returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Don't fail if incident API is unavailable
        print(f"  Warning: Could not reach incident API at {api_url}: {e}")
