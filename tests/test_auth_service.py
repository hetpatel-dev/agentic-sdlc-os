"""
test_auth_service.py - Unit and Integration Tests for AuthService and AuthAPI
Traces: REQ-101, REQ-102
"""

import time
import unittest
from src.auth.service import (
    AuthService,
    InvalidTokenError,
    TokenExpiredError
)
from src.auth.api import AuthAPI

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.mock_secret_key = "test_key_for_unit_tests"  # nosec
        self.username = "alice_engineer"
        self.sample_credential = "mock_user_pass_val"  # nosec

    def test_hash_and_verify_password(self):
        """@traces REQ-101: Password verification should succeed with correct password."""
        stored_hash = AuthService.hash_password(self.sample_credential)
        self.assertIn("$", stored_hash)
        self.assertTrue(AuthService.verify_password(self.sample_credential, stored_hash))
        self.assertFalse(AuthService.verify_password("wrong_candidate_val", stored_hash))
        self.assertFalse(AuthService.verify_password(self.sample_credential, "corrupted$hash"))
        self.assertFalse(AuthService.verify_password("", stored_hash))

    def test_salt_is_cryptographically_unique(self):
        """@traces REQ-101: Successive hashes of the same password produce distinct salts."""
        h1 = AuthService.hash_password(self.sample_credential)
        h2 = AuthService.hash_password(self.sample_credential)
        self.assertNotEqual(h1, h2)

    def test_issue_token_success(self):
        """@traces REQ-101: Issuing token returns signed token string and expiration."""
        token, expires_at = AuthService.issue_token(self.username, self.mock_secret_key, ttl_seconds=300)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split('.')), 3)
        self.assertGreater(expires_at, int(time.time()))

    def test_reserved_claims_protection(self):
        """@traces REQ-101: Caller-provided claims cannot overwrite sub or exp."""
        malicious_claims = {"sub": "impersonated_admin", "exp": 9999999999, "role": "developer"}
        token, _ = AuthService.issue_token(self.username, self.mock_secret_key, claims=malicious_claims)
        payload = AuthService.verify_token(token, self.mock_secret_key)
        self.assertEqual(payload["sub"], self.username)
        self.assertEqual(payload["role"], "developer")
        self.assertLess(payload["exp"], 9999999999)

    def test_verify_token_success(self):
        """@traces REQ-102: Verifying valid token returns user claims."""
        token, _ = AuthService.issue_token(self.username, self.mock_secret_key, claims={"role": "admin"})
        payload = AuthService.verify_token(token, self.mock_secret_key)
        self.assertEqual(payload["sub"], self.username)
        self.assertEqual(payload["role"], "admin")
        self.assertIn("exp", payload)

    def test_verify_token_tampered_signature(self):
        """@traces REQ-102: Modifying token payload or signature fails validation."""
        token, _ = AuthService.issue_token(self.username, self.mock_secret_key)
        parts = token.split('.')
        # Tamper payload
        tampered_token = f"{parts[0]}.eyJzdWIiOiJoYWNrZXIifQ.{parts[2]}"
        with self.assertRaises(InvalidTokenError):
            AuthService.verify_token(tampered_token, self.mock_secret_key)

    def test_verify_token_unsupported_header(self):
        """@traces REQ-102: Tokens with invalid or non-HS256 headers are rejected."""
        # Header with alg=none
        invalid_header_b64 = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0"
        payload_b64 = "eyJzdWIiOiJhbGljZSIsImV4cCI6OTk5OTk5OTk5OX0"
        fake_token = f"{invalid_header_b64}.{payload_b64}.c2ln"
        with self.assertRaises(InvalidTokenError):
            AuthService.verify_token(fake_token, self.mock_secret_key)

    def test_verify_token_expired(self):
        """@traces REQ-102: Expired token raises TokenExpiredError."""
        token, _ = AuthService.issue_token(self.username, self.mock_secret_key, ttl_seconds=-10)
        with self.assertRaises(TokenExpiredError):
            AuthService.verify_token(token, self.mock_secret_key)

    def test_empty_arguments_validation(self):
        """@traces REQ-101, REQ-102: Empty credentials raise ValueError."""
        with self.assertRaises(ValueError):
            AuthService.hash_password("")
        with self.assertRaises(ValueError):
            AuthService.issue_token("", self.mock_secret_key)
        with self.assertRaises(InvalidTokenError):
            AuthService.verify_token("", self.mock_secret_key)
        with self.assertRaises(InvalidTokenError):
            AuthService.verify_token("invalid_single_part", self.mock_secret_key)

    def test_api_controller_endpoints(self):
        """@traces REQ-101, REQ-102: AuthAPI login and verify endpoints handle 200, 400, 401."""
        stored_hash = AuthService.hash_password(self.sample_credential)
        user_db = {self.username: stored_hash}

        # Valid login -> 200
        code, body = AuthAPI.login({"username": self.username, "password": self.sample_credential}, self.mock_secret_key, user_db)
        self.assertEqual(code, 200)
        self.assertIn("token", body)
        token = body["token"]

        # Invalid password -> 401
        code, body = AuthAPI.login({"username": self.username, "password": "wrong_pass_val"}, self.mock_secret_key, user_db)
        self.assertEqual(code, 401)

        # Missing input -> 400
        code, body = AuthAPI.login({"username": ""}, self.mock_secret_key, user_db)
        self.assertEqual(code, 400)

        # Valid verify -> 200
        code, body = AuthAPI.verify(f"Bearer {token}", self.mock_secret_key)
        self.assertEqual(code, 200)
        self.assertEqual(body["claims"]["sub"], self.username)

        # Invalid verify -> 401
        code, body = AuthAPI.verify("Bearer invalid.token.signature", self.mock_secret_key)
        self.assertEqual(code, 401)

if __name__ == "__main__":
    unittest.main()
