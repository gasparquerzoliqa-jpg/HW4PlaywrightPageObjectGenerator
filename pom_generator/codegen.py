"""Code generation for POM classes."""


def generate_pom_class(located_elements, class_name='PageObject'):
    """
    Generate Python code for a Page Object Model class.

    Args:
        located_elements: List of LocatedElement namedtuples (name, element, locator)
        class_name: Name for the generated class (default: 'PageObject')

    Returns:
        Generated Python code as a string
    """
    lines = []

    lines.append('from playwright.sync_api import Page')
    lines.append('')
    lines.append('')
    lines.append(f'class {class_name}:')
    lines.append('    def __init__(self, page: Page):')

    if located_elements:
        for located_elem in located_elements:
            name = located_elem.name
            locator = located_elem.locator
            method = locator['method']
            value = locator['value']

            escaped_value = value.replace("'", "\\'")

            if method == 'get_by_test_id':
                locator_call = f"page.get_by_test_id('{escaped_value}')"
            elif method == 'get_by_role':
                if 'name' in locator:
                    escaped_name = locator['name'].replace("'", "\\'")
                    locator_call = f"page.get_by_role('{escaped_value}', name='{escaped_name}')"
                else:
                    locator_call = f"page.get_by_role('{escaped_value}')"
            elif method == 'get_by_label':
                locator_call = f"page.get_by_label('{escaped_value}')"
            elif method == 'get_by_placeholder':
                locator_call = f"page.get_by_placeholder('{escaped_value}')"
            elif method == 'get_by_text':
                locator_call = f"page.get_by_text('{escaped_value}')"
            elif method == 'locator':
                locator_call = f"page.locator('{escaped_value}')"
            else:
                locator_call = f"page.locator('{escaped_value}')"

            lines.append(f'        self.{name} = {locator_call}')
    else:
        lines.append('        self.page = page')

    return '\n'.join(lines)
