"""
api.py - HTTP Controller / API Layer for Authentication Service
Implements REST API endpoints defined in docs/api/auth-v1.yaml conforming to PRD-101.
"""

from typing import Dict, Any, Tuple
from src.auth.service import AuthService, InvalidTokenError, TokenExpiredError, InvalidCredentialsError

class AuthAPI:
    """REST API Controller implementing /auth/login and /auth/verify."""

    @staticmethod
    def login(payload: Dict[str, Any], secret_key: str, user_store: Dict[str, str]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /auth/login
        Implements REQ-101 and auth-v1.yaml.
        """
        if not isinstance(payload, dict):
            return 400, {"error": "Invalid request payload; expected JSON object."}

        username = payload.get("username")
        password = payload.get("password")

        if not username or not password or not isinstance(username, str) or not isinstance(password, str):
            return 400, {"error": "Username and password are required string fields."}

        if len(username) < 3 or len(username) > 50:
            return 400, {"error": "Username must be between 3 and 50 characters."}

        stored_hash = user_store.get(username)
        if not stored_hash or not AuthService.verify_password(password, stored_hash):
            return 401, {"error": "Invalid username or password."}

        token, expires_at = AuthService.issue_token(username, secret_key, ttl_seconds=900)
        return 200, {
            "token": token,
            "expires_at": expires_at
        }

    @staticmethod
    def verify(authorization_header: str, secret_key: str) -> Tuple[int, Dict[str, Any]]:
        """
        GET /auth/verify or Bearer Token Verification
        Implements REQ-102.
        """
        if not authorization_header or not isinstance(authorization_header, str):
            return 401, {"error": "Missing Authorization header."}

        parts = authorization_header.strip().split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return 401, {"error": "Invalid Authorization header format; expected 'Bearer <token>'."}

        token = parts[1].strip()
        try:
            claims = AuthService.verify_token(token, secret_key)
            return 200, {"claims": claims}
        except (InvalidTokenError, TokenExpiredError) as e:
            return 401, {"error": str(e)}
