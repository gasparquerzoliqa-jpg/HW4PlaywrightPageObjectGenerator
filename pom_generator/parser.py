"""HTML parsing and element detection."""
from collections import namedtuple
from pathlib import Path
from bs4 import BeautifulSoup
from . import NoElementsFoundError

Element = namedtuple('Element', ['type', 'tag', 'attributes'])


def parse_html(html_path):
    """
    Parse HTML and extract interactive elements.

    Args:
        html_path: Path to HTML file or empty string

    Returns:
        List of Element namedtuples

    Raises:
        NoElementsFoundError: If no interactive elements found
    """
    if html_path == "":
        raise NoElementsFoundError("No interactive elements found in HTML.")

    path = Path(html_path)
    html_content = path.read_text()

    soup = BeautifulSoup(html_content, 'html.parser')

    elements = []

    for tag in soup.find_all(['input', 'button', 'a', 'textarea', 'select']):
        element_type = None
        attrs = {}

        if tag.name == 'input':
            element_type = 'input'
            attrs = dict(tag.attrs)
        elif tag.name == 'button':
            element_type = 'button'
            attrs = dict(tag.attrs)
            if tag.string:
                attrs['text'] = tag.string
        elif tag.name == 'a':
            element_type = 'link'
            attrs = dict(tag.attrs)
            if tag.string:
                attrs['text'] = tag.string
        elif tag.name == 'textarea':
            element_type = 'textarea'
            attrs = dict(tag.attrs)
        elif tag.name == 'select':
            element_type = 'select'
            attrs = dict(tag.attrs)

        if element_type:
            elements.append(Element(type=element_type, tag=tag.name, attributes=attrs))

    if not elements:
        raise NoElementsFoundError("No interactive elements found in HTML.")

    return elements
