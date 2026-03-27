"""
Authentication Service Module

This module provides authentication validation functionality.
Contains an intentional bug for AutoSRE demonstration purposes.
"""


def validate_auth(request):
    """
    Validates authorization header from request.
    
    BUG: Missing null check on authorization header - will raise TypeError
    when Authorization header is None.
    """
    # INTENTIONAL BUG: No null check before accessing header
    auth_header = request.headers.get('Authorization')
    # Bug is on line 18-19: attempting to use None value in string operation
    token_parts = auth_header.split(' ')  # AttributeError: 'NoneType' object has no attribute 'split'
    
    if len(token_parts) != 2:
        return False
    
    scheme, token = token_parts
    
    if scheme.lower() != 'bearer':
        return False
    
    # Simplified validation - just check token is not empty
    return len(token) > 0
