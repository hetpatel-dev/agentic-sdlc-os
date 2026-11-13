"""
service.py - Authentication and Cryptographic Token Service
Implements REQ-101 (User Authentication) and REQ-102 (Token Verification).
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Dict, Any, Tuple, Optional

class AuthError(Exception):
    """Base exception for authentication failures."""
    pass

class InvalidCredentialsError(AuthError):
    """Raised when user credentials fail verification."""
    pass

class InvalidTokenError(AuthError):
    """Raised when token signature or payload is invalid."""
    pass

class TokenExpiredError(AuthError):
    """Raised when token has exceeded its expiration timestamp."""
    pass

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def _base64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data.encode('ascii'))

class AuthService:
    """Core authentication service for password hashing and token management."""

    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> str:
        """Hashes a password using PBKDF2-HMAC-SHA256 with cryptographically secure salt."""
        if not password:
            raise ValueError("Password cannot be empty.")
        if salt is None:
            salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        return f"{_base64url_encode(salt)}${_base64url_encode(dk)}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verifies candidate password against stored salt and hash."""
        if not password or not stored_hash or '$' not in stored_hash:
            return False
        try:
            salt_b64, hash_b64 = stored_hash.split('$', 1)
            salt = _base64url_decode(salt_b64)
            expected_dk = _base64url_decode(hash_b64)
            actual_dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
            return hmac.compare_digest(actual_dk, expected_dk)
        except Exception:
            return False

    @staticmethod
    def issue_token(subject: str, secret_key: str, ttl_seconds: int = 900, claims: Optional[Dict[str, Any]] = None) -> Tuple[str, int]:
        """
        Issues a cryptographically signed token (HMAC-SHA256).
        Implements REQ-101.
        """
        if not subject:
            raise ValueError("Subject cannot be empty.")
        if not secret_key:
            raise ValueError("Secret key cannot be empty.")

        now = int(time.time())
        expires_at = now + ttl_seconds
        payload = {
            "sub": subject,
            "iat": now,
            "exp": expires_at
        }
        if claims:
            # Prevent reserved claims from being overwritten
            reserved = {"sub", "iat", "exp"}
            safe_claims = {k: v for k, v in claims.items() if k not in reserved}
            payload.update(safe_claims)

        header = {"alg": "HS256", "typ": "JWT"}
        h_bytes = json.dumps(header, separators=(',', ':')).encode('utf-8')
        p_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')

        signing_input = f"{_base64url_encode(h_bytes)}.{_base64url_encode(p_bytes)}"
        signature = hmac.new(secret_key.encode('utf-8'), signing_input.encode('ascii'), hashlib.sha256).digest()
        token = f"{signing_input}.{_base64url_encode(signature)}"
        return token, expires_at

    @staticmethod
    def verify_token(token: str, secret_key: str) -> Dict[str, Any]:
        """
        Verifies signature, header algorithm, and expiration of a signed token.
        Implements REQ-102.
        """
        if not token or not secret_key:
            raise InvalidTokenError("Token and secret key are required.")

        parts = token.split('.')
        if len(parts) != 3:
            raise InvalidTokenError("Malformed token structure.")

        h_b64, p_b64, sig_b64 = parts
        signing_input = f"{h_b64}.{p_b64}"

        # 1. Validate JWT Header
        try:
            header = json.loads(_base64url_decode(h_b64).decode('utf-8'))
        except Exception as e:
            raise InvalidTokenError("Invalid token header encoding.") from e

        if not isinstance(header, dict) or header.get("alg") != "HS256" or header.get("typ") != "JWT":
            raise InvalidTokenError("Unsupported token header or algorithm.")

        # 2. Verify Cryptographic Signature
        expected_sig = hmac.new(secret_key.encode('utf-8'), signing_input.encode('ascii'), hashlib.sha256).digest()
        try:
            actual_sig = _base64url_decode(sig_b64)
        except Exception as e:
            raise InvalidTokenError("Invalid token signature encoding.") from e

        if not hmac.compare_digest(actual_sig, expected_sig):
            raise InvalidTokenError("Token signature mismatch.")

        # 3. Decode & Verify Payload
        try:
            payload = json.loads(_base64url_decode(p_b64).decode('utf-8'))
        except Exception as e:
            raise InvalidTokenError("Invalid token payload encoding.") from e

        if not isinstance(payload, dict):
            raise InvalidTokenError("Token payload must be a JSON object.")

        now = int(time.time())
        exp = payload.get("exp")
        if exp is None or not isinstance(exp, (int, float)) or exp < now:
            raise TokenExpiredError("Token has expired.")

        return payload
