"""
Trigger Errors Script

This script simulates production traffic to the Dummy Error App,
intentionally triggering authentication and database connection bugs.
"""

import requests
import time


BASE_URL = "http://localhost:8080"


def trigger_auth_bug():
    """
    Triggers authentication bug by sending POST request without Authorization header.
    This causes a TypeError in auth_service.py due to missing null check.
    """
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "testuser", "password": "testpass"},
            timeout=5
        )
        print(f"Auth bug trigger: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Auth request failed: {e}")


def trigger_db_bug():
    """
    Triggers database connection leak by sending multiple rapid requests.
    This exhausts the connection pool (max 5 connections) due to missing finally block.
    """
    print("Triggering DB bug with rapid requests...")
    for i in range(12):
        try:
            response = requests.get(f"{BASE_URL}/api/data", timeout=5)
            print(f"  Request {i+1}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  Request {i+1} failed: {e}")
        # Small delay between requests
        time.sleep(0.1)


def run_traffic_simulation():
    """
    Main loop that continuously triggers errors to simulate production traffic.
    Alternates between auth bug and database bug with delays.
    """
    print("Starting traffic simulation...")
    print(f"Target: {BASE_URL}")
    print("Press Ctrl+C to stop\n")
    
    cycle = 0
    while True:
        cycle += 1
        print(f"\n=== Cycle {cycle} ===")
        
        # Trigger authentication bug
        print("Triggering authentication bug...")
        trigger_auth_bug()
        
        # Delay between different error types
        time.sleep(2)
        
        # Trigger database connection bug
        trigger_db_bug()
        
        # Delay before next cycle
        print(f"\nWaiting 5 seconds before next cycle...")
        time.sleep(5)


if __name__ == "__main__":
    run_traffic_simulation()
