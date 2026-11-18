import pytest
from pathlib import Path
from pom_generator.parser import parse_html
from pom_generator import NoElementsFoundError


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


class TestParserDetectElements:
    def test_detect_inputs(self, fixtures_dir):
        html_path = fixtures_dir / "simple_form.html"
        elements = parse_html(html_path)

        input_elements = [e for e in elements if e.type == 'input']
        assert len(input_elements) >= 2
        assert any(e.attributes.get('type') == 'text' for e in input_elements)
        assert any(e.attributes.get('type') == 'password' for e in input_elements)

    def test_detect_buttons(self, fixtures_dir):
        html_path = fixtures_dir / "simple_form.html"
        elements = parse_html(html_path)

        button_elements = [e for e in elements if e.type == 'button']
        assert len(button_elements) >= 1

    def test_detect_links(self, fixtures_dir):
        html_path = fixtures_dir / "simple_form.html"
        elements = parse_html(html_path)

        link_elements = [e for e in elements if e.type == 'link']
        assert len(link_elements) >= 1

    def test_extract_attributes(self, fixtures_dir):
        html_path = fixtures_dir / "simple_form.html"
        elements = parse_html(html_path)

        username_input = next(
            (e for e in elements if e.attributes.get('id') == 'username'),
            None
        )
        assert username_input is not None
        assert username_input.attributes.get('placeholder') == 'Enter username'
        assert username_input.attributes.get('type') == 'text'

    def test_empty_html_raises_error(self, fixtures_dir):
        html_path = fixtures_dir / "empty.html"
        with pytest.raises(NoElementsFoundError) as exc_info:
            parse_html(html_path)
        assert "No interactive elements found in HTML" in str(exc_info.value)

    def test_returns_element_namedtuple(self, fixtures_dir):
        html_path = fixtures_dir / "simple_form.html"
        elements = parse_html(html_path)

        assert elements is not None
        assert len(elements) > 0

        element = elements[0]
        assert hasattr(element, 'type')
        assert hasattr(element, 'tag')
        assert hasattr(element, 'attributes')
        assert isinstance(element.attributes, dict)

    def test_detect_textarea(self, fixtures_dir):
        html_path = fixtures_dir / "semantic_html.html"
        elements = parse_html(html_path)

        textarea_elements = [e for e in elements if e.type == 'textarea']
        assert len(textarea_elements) >= 1

    def test_detect_checkboxes(self, fixtures_dir):
        html_path = fixtures_dir / "complex_form.html"
        elements = parse_html(html_path)

        checkbox_elements = [e for e in elements if e.attributes.get('type') == 'checkbox']
        assert len(checkbox_elements) >= 1

    def test_detect_radio_buttons(self, fixtures_dir):
        html_path = fixtures_dir / "complex_form.html"
        elements = parse_html(html_path)

        radio_elements = [e for e in elements if e.attributes.get('type') == 'radio']
        assert len(radio_elements) >= 2

    def test_empty_string_html_raises_error(self):
        with pytest.raises(NoElementsFoundError) as exc_info:
            parse_html("")
        assert "No interactive elements found in HTML" in str(exc_info.value)
