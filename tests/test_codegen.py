import pytest
import ast
from collections import namedtuple
from pom_generator.codegen import generate_pom_class

Element = namedtuple('Element', ['type', 'tag', 'attributes'])
LocatedElement = namedtuple('LocatedElement', ['name', 'element', 'locator'])


class TestCodeGeneration:
    def test_generates_valid_python_class(self):
        elements = [
            LocatedElement(
                name='submit_button',
                element=Element('button', 'button', {'id': 'submit'}),
                locator={'strategy': 'test_id', 'value': 'submit', 'method': 'get_by_test_id'}
            )
        ]
        code = generate_pom_class(elements, class_name='LoginPage')

        assert code is not None
        assert isinstance(code, str)
        # Try to parse as valid Python
        try:
            ast.parse(code)
        except SyntaxError:
            pytest.fail(f"Generated code is not valid Python:\n{code}")

    def test_class_name_configurable(self):
        elements = []
        code = generate_pom_class(elements, class_name='CustomPageObject')

        assert 'class CustomPageObject' in code

    def test_default_class_name_is_pageobject(self):
        elements = []
        code = generate_pom_class(elements)

        assert 'class PageObject' in code

    def test_includes_all_attributes_in_init(self):
        elements = [
            LocatedElement(
                name='username_input',
                element=Element('input', 'input', {'id': 'username'}),
                locator={'strategy': 'test_id', 'value': 'username', 'method': 'get_by_test_id'}
            ),
            LocatedElement(
                name='submit_button',
                element=Element('button', 'button', {'id': 'submit'}),
                locator={'strategy': 'test_id', 'value': 'submit', 'method': 'get_by_test_id'}
            )
        ]
        code = generate_pom_class(elements, class_name='LoginPage')

        assert 'self.username_input' in code
        assert 'self.submit_button' in code
        assert '@property' not in code

    def test_uses_correct_locator_method_in_init(self):
        elements = [
            LocatedElement(
                name='submit_btn',
                element=Element('button', 'button', {'data-testid': 'submit'}),
                locator={'strategy': 'test_id', 'value': 'submit', 'method': 'get_by_test_id'}
            )
        ]
        code = generate_pom_class(elements, class_name='TestPage')

        assert 'self.submit_btn = page.get_by_test_id' in code or 'self.submit_btn=page.get_by_test_id' in code
        assert "'submit'" in code or '"submit"' in code

    def test_includes_page_parameter_in_constructor(self):
        elements = []
        code = generate_pom_class(elements, class_name='TestPage')

        assert 'def __init__' in code
        assert 'page' in code or 'self.page' in code

    def test_imports_playwright(self):
        elements = []
        code = generate_pom_class(elements)

        assert 'from playwright' in code or 'import' in code

    def test_empty_elements_generates_valid_class(self):
        elements = []
        code = generate_pom_class(elements, class_name='EmptyPage')

        assert 'class EmptyPage' in code
        assert 'def __init__' in code
        try:
            ast.parse(code)
        except SyntaxError:
            pytest.fail(f"Generated empty class is not valid Python:\n{code}")

    def test_handles_multiple_elements(self):
        elements = [
            LocatedElement(
                name='username',
                element=Element('input', 'input', {'id': 'user'}),
                locator={'strategy': 'test_id', 'value': 'user', 'method': 'get_by_test_id'}
            ),
            LocatedElement(
                name='password',
                element=Element('input', 'input', {'id': 'pass'}),
                locator={'strategy': 'test_id', 'value': 'pass', 'method': 'get_by_test_id'}
            ),
            LocatedElement(
                name='login_button',
                element=Element('button', 'button', {'id': 'login'}),
                locator={'strategy': 'test_id', 'value': 'login', 'method': 'get_by_test_id'}
            ),
        ]
        code = generate_pom_class(elements, class_name='LoginPage')

        assert 'self.username' in code
        assert 'self.password' in code
        assert 'self.login_button' in code

    def test_no_property_decorators(self):
        elements = [
            LocatedElement(
                name='submit_button',
                element=Element('button', 'button', {'id': 'submit'}),
                locator={'strategy': 'test_id', 'value': 'submit', 'method': 'get_by_test_id'}
            )
        ]
        code = generate_pom_class(elements, class_name='FormPage')

        assert '@property' not in code
        assert 'def submit_button' not in code
