"""
Generator Logic Module for Random Password Generator
Implements cryptographically secure password generation using Python's secrets module,
diversity enforcement rules, ambiguous character filtering, and entropy-based strength calculation.
"""

import secrets
import string
import math
from typing import Tuple, Dict, Any, List

AMBIGUOUS_CHARS = set("0Oo1lI|")

def generate_password(
    length: int = 12,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> Tuple[bool, str]:
    """
    Generates a cryptographically secure random password based on specified criteria.

    Args:
        length: Password length (must be >= 8).
        use_upper: Include uppercase letters (A-Z).
        use_lower: Include lowercase letters (a-z).
        use_digits: Include numeric digits (0-9).
        use_symbols: Include special symbols (!@#$%^&*...).
        exclude_ambiguous: Exclude ambiguous characters (0, O, o, 1, l, I, |).

    Returns:
        (success: bool, result_or_error: str)
    """
    # 1. Minimum length validation
    if length < 8:
        return False, "Password length must be at least 8 characters."

    # 2. Build character pools
    pools: List[str] = []

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(chars)

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(chars)

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(chars)

    if use_symbols:
        chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(chars)

    # 3. Require at least 2 character pools
    if len(pools) < 2:
        return False, "Please select at least 2 character types (Uppercase, Lowercase, Numbers, Symbols)."

    # 4. Ensure each selected pool has remaining characters after filtering
    for pool in pools:
        if not pool:
            return False, "Character pool became empty after excluding ambiguous characters."

    # 5. Security Rule: Guarantee at least 1 character from EACH selected pool
    password_chars = []
    for pool in pools:
        password_chars.append(secrets.choice(pool))

    # 6. Fill remaining slots from combined pool
    combined_pool = "".join(pools)
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(combined_pool))

    # 7. Securely shuffle the password list
    secrets.SystemRandom().shuffle(password_chars)

    return True, "".join(password_chars)


def calculate_strength(
    password: str,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> Dict[str, Any]:
    """
    Calculates password entropy and returns visual strength parameters.

    Returns:
        Dict with keys: 'score', 'label', 'color', 'entropy'
    """
    if not password:
        return {'score': 0, 'label': 'None', 'color': '#CBD5E0', 'entropy': 0.0}

    # Calculate pool size N
    pool_size = 0
    if use_lower:
        pool_size += 26 - (3 if exclude_ambiguous else 0)
    if use_upper:
        pool_size += 26 - (3 if exclude_ambiguous else 0)
    if use_digits:
        pool_size += 10 - (2 if exclude_ambiguous else 0)
    if use_symbols:
        pool_size += 26 - (1 if exclude_ambiguous else 0)

    if pool_size <= 0:
        pool_size = 26

    length = len(password)
    entropy = length * math.log2(pool_size)

    # Classification
    if entropy < 40 or length < 10:
        return {
            'score': 25,
            'label': 'Weak ⚠️',
            'color': '#E53E3E', # Red
            'entropy': round(entropy, 1)
        }
    elif entropy < 60:
        return {
            'score': 50,
            'label': 'Medium ⚡',
            'color': '#DD6B20', # Orange
            'entropy': round(entropy, 1)
        }
    elif entropy < 80:
        return {
            'score': 75,
            'label': 'Strong 🔒',
            'color': '#38A169', # Green
            'entropy': round(entropy, 1)
        }
    else:
        return {
            'score': 100,
            'label': 'Very Strong (Bulletproof) 🛡️',
            'color': '#3182CE', # Blue/Teal
            'entropy': round(entropy, 1)
        }
