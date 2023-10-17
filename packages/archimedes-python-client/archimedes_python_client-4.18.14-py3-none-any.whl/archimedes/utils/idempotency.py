"""
Helper functions for idempotency
"""
import uuid


def generate_idempotency_key() -> str:
    """
    Generate a unique idempotency key.
    """
    return uuid.uuid4().hex
