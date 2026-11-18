# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**POM Generator** — A tool that parses HTML snippets and generates Playwright Page Object Model (POM) classes in Python. This tool is designed to accelerate test automation by automatically discovering interactive elements and generating attributes for each element with semantic locators.

## Directory Structure

```
pom-generator/
├── generate.py              # CLI entry point
├── tests/
│   ├── test_parser.py       # HTML parsing tests
│   ├── test_locator.py      # Locator selection logic tests
│   ├── test_codegen.py      # Code generation tests
│   └── fixtures/            # Test HTML files
├── pom_generator/
│   ├── __init__.py
│   ├── parser.py            # HTML parsing and element detection
│   ├── locator.py           # Locator strategy selection
│   ├── codegen.py           # Python code generation
│   └── validator.py         # Attribute name validation
├── output/                  # Generated POM classes (gitignored)
└── venv/                    # Virtual environment
```

## Locator Priority Strategy

Locators are selected in this priority order (first match wins), using Playwright's semantic locator methods:

1. **Test ID** — `page.get_by_test_id()` for explicit test markers (`data-testid` attribute)
2. **Role** — `page.get_by_role()` for semantic HTML roles (buttons, links, forms, etc.)
3. **Label** — `page.get_by_label()` for form fields with associated labels
4. **Placeholder** — `page.get_by_placeholder()` for input placeholder text
5. **Text** — `page.get_by_text()` for button/link text content
6. **CSS Locator** — `page.locator()` with CSS selectors only as a last resort

## Development Commands

```bash
# Activate venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run a specific test file
pytest tests/test_parser.py

# Run a specific test
pytest tests/test_parser.py::test_detect_inputs

# Run tests
pytest tests/

# Run the tool
python generate.py path/to/file.html [--class-name MyPageObject]
```

## Architecture Notes

**Parser** (`parser.py`) — Parses HTML with BeautifulSoup, discovers interactive elements (inputs, buttons, links), and extracts their attributes. Returns a list of `Element` namedtuples containing type, tag, attributes.

**Locator** (`locator.py`) — Takes an Element and returns the best locator strategy and value based on the priority list. Handles conflicts (duplicates) by appending numeric suffixes.

**CodeGen** (`codegen.py`) — Generates Python class code with:
  - An `__init__(self, page)` constructor that accepts a Playwright `Page` object
  - Instance attributes for each element (e.g., `self.submit_button = page.get_by_test_id(...)`)
  - Each attribute assigned using semantic Playwright locator methods (`page.get_by_test_id()`, `page.get_by_role()`, `page.get_by_label()`, `page.get_by_placeholder()`, `page.get_by_text()`, or `page.locator()` as fallback)

**Validator** (`validator.py`) — Ensures attribute names are valid Python identifiers, unique, and handles duplicates with numeric suffixes.

## Key Implementation Details

- **Empty HTML handling** — Raise a clear `NoElementsFoundError` with message: "No interactive elements found in HTML."
- **Attribute naming** — Snake_case conversion; duplicates get `_2`, `_3` suffixes in discovery order
- **Classname configuration** — Default to `"PageObject"`, override with `--class-name` flag
- **Output format** — Generated file named `{classname}.py`, saved to `output/` folder

## Testing Strategy

Write tests in this order:
1. Parser: detect inputs, buttons, links; extract attributes
2. Locator: priority selection; duplicate handling
3. CodeGen: class structure, method signatures, formatting
4. Integration: end-to-end CLI with sample HTML files
5. Edge cases: empty HTML, malformed HTML, missing attributes
