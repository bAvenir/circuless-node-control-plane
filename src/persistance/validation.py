import re

def validate_wot_urn(urn: str) -> bool:
    """Validate URN format according to RFC 8141"""
    # Basic URN pattern matching
    pattern = r'^urn:[a-zA-Z0-9][a-zA-Z0-9\-]{0,30}[a-zA-Z0-9]:[^?#]+$'
    return bool(re.match(pattern, urn))