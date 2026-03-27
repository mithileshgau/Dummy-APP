"""
Dummy Error App - Flask Application

This Flask application intentionally contains bugs for AutoSRE demonstration.
It exposes endpoints that trigger authentication and database connection errors.
"""

from flask import Flask, request, jsonify
import auth_service
import db_connection
import error_logger


def create_app():
    """Initialize and configure Flask application"""
    app = Flask(__name__)
    
    # Error handling middleware
    @app.errorhandler(Exception)
    def handle_error(error):
        """Catch all exceptions and log them"""
        # Get endpoint from request
        endpoint = request.path if request else "unknown"
        context = {"endpoint": endpoint}
        
        # Log error to console and incident API
        error_logger.log_error(error, context)
        
        # Return error response but keep app running
        return jsonify({
            "error": type(error).__name__,
            "details": str(error)
        }), 500
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy"}), 200
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        """Authentication endpoint that triggers auth bug"""
        # This will trigger TypeError when Authorization header is missing
        is_valid = auth_service.validate_auth(request)
        
        if is_valid:
            return jsonify({"success": True, "token": "dummy_token"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    @app.route('/api/data', methods=['GET'])
    def get_data():
        """Data retrieval endpoint that triggers database bug"""
        # This will trigger connection leak and eventual pool exhaustion
        data = db_connection.query_data()
        return jsonify({"data": data}), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Startup logging message
    print("Starting Dummy Error App on port 8080...")
    print("Endpoints available:")
    print("  GET  /health      - Health check")
    print("  POST /auth/login  - Authentication (triggers TypeError bug)")
    print("  GET  /api/data    - Data retrieval (triggers connection leak bug)")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=8080, debug=False)
