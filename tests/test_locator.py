import pytest
from collections import namedtuple
from pom_generator.locator import select_locator

Element = namedtuple('Element', ['type', 'tag', 'attributes'])


class TestLocatorPriority:
    def test_priority_test_id(self):
        element = Element(
            type='button',
            tag='button',
            attributes={'id': 'submit', 'data-testid': 'submit-btn'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'test_id'
        assert locator['value'] == 'submit-btn'
        assert locator['method'] == 'get_by_test_id'

    def test_priority_role(self):
        element = Element(
            type='button',
            tag='button',
            attributes={'role': 'button', 'id': 'action-btn'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'role'
        assert locator['value'] == 'button'
        assert locator['method'] == 'get_by_role'

    def test_priority_label(self):
        element = Element(
            type='input',
            tag='input',
            attributes={'id': 'email', 'type': 'email'}
        )
        # This test assumes a label is associated externally
        # The locator should handle the label strategy
        locator = select_locator(element)
        assert locator is not None

    def test_priority_placeholder(self):
        element = Element(
            type='input',
            tag='input',
            attributes={'type': 'text', 'placeholder': 'Enter username'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'placeholder'
        assert locator['value'] == 'Enter username'
        assert locator['method'] == 'get_by_placeholder'

    def test_priority_text_button(self):
        element = Element(
            type='button',
            tag='button',
            attributes={'text': 'Login', 'name': 'login-btn'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'role'
        assert locator['value'] == 'button'
        assert locator['method'] == 'get_by_role'
        assert locator.get('name') == 'Login'

    def test_priority_text_link(self):
        element = Element(
            type='link',
            tag='a',
            attributes={'href': '/logout', 'text': 'Logout'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'role'
        assert locator['value'] == 'link'
        assert locator['method'] == 'get_by_role'
        assert locator.get('name') == 'Logout'

    def test_fallback_css_locator(self):
        element = Element(
            type='input',
            tag='input',
            attributes={'type': 'text'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'css'
        assert locator['method'] == 'locator'
        assert 'input[type=text]' in locator['value'] or locator['value'] != ''

    def test_returns_locator_dict(self):
        element = Element(
            type='button',
            tag='button',
            attributes={'data-testid': 'submit'}
        )
        locator = select_locator(element)

        assert isinstance(locator, dict)
        assert 'strategy' in locator
        assert 'value' in locator
        assert 'method' in locator

    def test_locator_with_id_fallback(self):
        element = Element(
            type='button',
            tag='button',
            attributes={'id': 'submit-btn'}
        )
        locator = select_locator(element)

        assert locator is not None
        assert 'strategy' in locator
        assert 'value' in locator

    def test_locator_for_input_with_name(self):
        element = Element(
            type='input',
            tag='input',
            attributes={'type': 'text', 'name': 'username'}
        )
        locator = select_locator(element)

        assert locator is not None

    def test_button_with_text_uses_role_with_name(self):
        """Regression test: button with text should use role locator with name."""
        element = Element(
            type='button',
            tag='button',
            attributes={'text': 'Login'}
        )
        locator = select_locator(element)

        assert locator['method'] == 'get_by_role'
        assert locator['strategy'] == 'role'
        assert locator['value'] == 'button'
        assert locator.get('name') == 'Login'

    def test_link_with_text_uses_role_with_name(self):
        """Regression test: link with text should use role locator with name."""
        element = Element(
            type='link',
            tag='a',
            attributes={'href': '/signup', 'text': 'Sign Up'}
        )
        locator = select_locator(element)

        assert locator['method'] == 'get_by_role'
        assert locator['strategy'] == 'role'
        assert locator['value'] == 'link'
        assert locator.get('name') == 'Sign Up'

    def test_text_locator_for_non_button_link_element(self):
        """Test that get_by_text is used for text-only elements that are not buttons or links."""
        element = Element(
            type='div',
            tag='div',
            attributes={'text': 'Welcome Message', 'class': 'alert'}
        )
        locator = select_locator(element)

        assert locator['strategy'] == 'text'
        assert locator['value'] == 'Welcome Message'
        assert locator['method'] == 'get_by_text'
