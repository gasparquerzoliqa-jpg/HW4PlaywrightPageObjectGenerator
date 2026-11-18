"""Attribute name validation and normalization."""
import re


def validate_and_normalize_names(names):
    """
    Convert names to snake_case and ensure uniqueness.

    Args:
        names: List of attribute names

    Returns:
        List of normalized, unique attribute names
    """
    if not names:
        return []

    def to_snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        s3 = re.sub(r'[^a-z0-9_]', '_', s2.lower())
        s4 = re.sub(r'_+', '_', s3).strip('_')
        return s4

    normalized = [to_snake_case(name) for name in names]

    result = []
    seen = {}
    for name in normalized:
        if name not in seen:
            seen[name] = 0
            result.append(name)
        else:
            seen[name] += 1
            result.append(f"{name}_{seen[name] + 1}")

    return result
