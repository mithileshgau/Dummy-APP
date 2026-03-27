"""
Database connection module with intentional connection leak bug.

This module manages database connections with a connection pool.
BUG: Missing finally block causes connection leaks and pool exhaustion.
"""

import time
from typing import Optional


class ConnectionPoolExhausted(Exception):
    """Raised when the connection pool has no available connections."""
    pass


class ConnectionPool:
    """Simple connection pool that tracks active connections."""
    
    def __init__(self, max_connections: int = 5):
        self.max_connections = max_connections
        self.active_connections = 0
        self.available_connections = max_connections
    
    def acquire(self):
        """Acquire a connection from the pool."""
        if self.available_connections <= 0:
            raise ConnectionPoolExhausted(
                f"Connection pool exhausted: {self.active_connections}/{self.max_connections} connections active"
            )
        
        self.available_connections -= 1
        self.active_connections += 1
        # Simulate connection object
        return {"connection_id": self.active_connections, "connected": True}
    
    def release(self, connection):
        """Release a connection back to the pool."""
        if connection and connection.get("connected"):
            self.active_connections -= 1
            self.available_connections += 1


# Global connection pool instance
_connection_pool = ConnectionPool(max_connections=5)


def get_connection():
    """
    Retrieves database connection from pool.
    
    BUG: Missing finally block to close connections properly.
    Connections are acquired but not reliably released, causing pool exhaustion.
    """
    connection = _connection_pool.acquire()
    
    # Simulate some connection setup work
    time.sleep(0.01)
    
    # BUG: No try-finally block here means if an error occurs,
    # or if the caller forgets to close, the connection leaks
    return connection


def query_data() -> list:
    """
    Executes database query using connection.
    
    BUG: Gets connection but doesn't close it in a finally block,
    causing connection leak on every call.
    """
    # BUG: Connection acquired here but not properly released
    connection = get_connection()
    
    # Simulate query execution
    time.sleep(0.02)
    
    # Return some dummy data
    data = [
        {"id": 1, "value": "data_1"},
        {"id": 2, "value": "data_2"},
        {"id": 3, "value": "data_3"}
    ]
    
    # BUG: Connection is NOT released here!
    # Should have: _connection_pool.release(connection) in a finally block
    # This causes the connection to leak
    
    return data
