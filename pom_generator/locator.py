"""Locator strategy selection."""


def select_locator(element):
    """
    Select the best locator strategy for an element.

    Locator priority order:
    1. Test ID (data-testid)
    2. Role (semantic HTML, including implicit roles from tag)
    3. Label (form fields)
    4. Placeholder (input hints)
    5. Text (button/link content as name in role locator)
    6. CSS Locator (fallback)

    Args:
        element: Element namedtuple with type, tag, attributes

    Returns:
        Dict with keys: strategy, value, method, and optional 'name' for role locators
    """
    attrs = element.attributes

    if 'data-testid' in attrs:
        return {
            'strategy': 'test_id',
            'value': attrs['data-testid'],
            'method': 'get_by_test_id'
        }

    if 'role' in attrs:
        return {
            'strategy': 'role',
            'value': attrs['role'],
            'method': 'get_by_role'
        }

    if 'placeholder' in attrs:
        return {
            'strategy': 'placeholder',
            'value': attrs['placeholder'],
            'method': 'get_by_placeholder'
        }

    if element.type == 'button' and 'text' in attrs:
        return {
            'strategy': 'role',
            'value': 'button',
            'method': 'get_by_role',
            'name': attrs['text']
        }

    if element.type == 'link' and 'text' in attrs:
        return {
            'strategy': 'role',
            'value': 'link',
            'method': 'get_by_role',
            'name': attrs['text']
        }

    if 'text' in attrs:
        return {
            'strategy': 'text',
            'value': attrs['text'],
            'method': 'get_by_text'
        }

    if 'id' in attrs:
        return {
            'strategy': 'css',
            'value': f"#{attrs['id']}",
            'method': 'locator'
        }

    if 'name' in attrs:
        return {
            'strategy': 'css',
            'value': f"{element.tag}[name='{attrs['name']}']",
            'method': 'locator'
        }

    if 'class' in attrs:
        classes = attrs['class']
        if isinstance(classes, list):
            class_str = '.'.join(classes)
        else:
            class_str = classes.replace(' ', '.')
        return {
            'strategy': 'css',
            'value': f"{element.tag}.{class_str}",
            'method': 'locator'
        }

    return {
        'strategy': 'css',
        'value': element.tag,
        'method': 'locator'
    }
