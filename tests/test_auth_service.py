"""
test_auth_service.py - Unit and Integration Tests for AuthService
Traces: REQ-101, REQ-102
"""

import time
import unittest
from src.auth.service import (
    AuthService,
    InvalidTokenError,
    TokenExpiredError
)

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

    def test_issue_token_success(self):
        """@traces REQ-101: Issuing token returns signed token string and expiration."""
        token, expires_at = AuthService.issue_token(self.username, self.mock_secret_key, ttl_seconds=300)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split('.')), 3)
        self.assertGreater(expires_at, int(time.time()))

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

    def test_verify_token_expired(self):
        """@traces REQ-102: Expired token raises TokenExpiredError."""
        # Issue token that expired 10 seconds ago
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

if __name__ == "__main__":
    unittest.main()
