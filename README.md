# POM Generator

**POM Generator** is a tool that parses HTML snippets and automatically generates Playwright Page Object Model (POM) classes in Python. It accelerates test automation by discovering interactive elements and generating semantic locators for each element.

## Installation

### Windows

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### macOS / Linux

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with an HTML file:

```bash
python generate.py path/to/file.html
```

### Options

- `--class-name` — Specify a custom class name (default: `PageObject`):
  ```bash
  python generate.py path/to/file.html --class-name LoginPage
  ```

## Input and Output Example

**Input** (`tests/fixtures/simple_form.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Simple Form</title>
</head>
<body>
    <form>
        <input type="text" id="username" placeholder="Enter username" />
        <input type="password" id="password" placeholder="Enter password" />
        <button type="submit">Login</button>
        <a href="/signup">Sign Up</a>
    </form>
</body>
</html>
```

**Output** (generated `PageObject.py`):
```python
from playwright.sync_api import Page


class PageObject:
    def __init__(self, page: Page):
        self.username = page.get_by_placeholder('Enter username')
        self.password = page.get_by_placeholder('Enter password')
        self.login = page.get_by_role('button', name='Login')
        self.sign_up = page.get_by_role('link', name='Sign Up')
```

The generated class can be used in tests:

```python
from playwright.sync_api import sync_playwright
from output.PageObject import PageObject

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://example.com")
    
    pom = PageObject(page)
    pom.username.fill("admin")
    pom.password.fill("password123")
    pom.login.click()
```

## Locator Priority

The tool selects locators in this priority order (first match wins):

1. **Test ID** — `page.get_by_test_id()` for `data-testid` attributes
2. **Role** — `page.get_by_role()` for semantic HTML roles
   - Buttons and links use `get_by_role()` with the `name` parameter for text content
3. **Placeholder** — `page.get_by_placeholder()` for input hints
4. **Text** — `page.get_by_text()` for element text content
5. **CSS** — `page.locator()` as a fallback using CSS selectors (by id, name, class, or tag)

## Running Tests

Run all tests with pytest:

```bash
python -m pytest tests/ -q
```

The test suite includes:
- **Parser tests** — HTML parsing, element detection (inputs, buttons, links, textareas, selects)
- **Locator tests** — Locator priority selection, role-based locators with names, CSS fallbacks
- **Code generation tests** — Class structure, method signatures, formatting
- **Integration tests** — End-to-end CLI workflows, file generation, error handling
- **Validator tests** — Attribute name normalization, snake_case conversion, duplicate handling

## Project Structure

```
pom-generator/
├── generate.py                  # CLI entry point
├── requirements.txt             # Project dependencies
├── CLAUDE.md                    # Development notes
├── README.md                    # This file
├── output/                      # Generated POM classes (gitignored)
├── pom_generator/
│   ├── __init__.py             # Exception definitions
│   ├── parser.py               # HTML parsing and element detection
│   ├── locator.py              # Locator strategy selection
│   ├── codegen.py              # Python code generation
│   └── validator.py            # Attribute name validation
├── tests/
│   ├── test_parser.py          # Parser functionality tests
│   ├── test_locator.py         # Locator selection tests
│   ├── test_codegen.py         # Code generation tests
│   ├── test_integration.py     # CLI integration tests
│   ├── test_validator.py       # Name validation tests
│   └── fixtures/               # Test HTML files
└── .venv/                      # Virtual environment
```

## MVP Limitations

The current implementation does not yet support:

- **TypeScript output** — Generated classes are Python only
- **Custom locator strategies** — Locator selection follows a fixed priority order
- **Live webpage validation** — Locators are not verified against a running webpage
- **Advanced CSS selectors** — Only basic CSS selectors are generated as fallbacks

### Known Observed Behaviors

- **Label-associated inputs** — Inputs with `<label for="...">` are not detected and fall back to `page.locator('#id')` CSS selectors instead of using `get_by_label()`
- **Buttons/links with indirect text** — Buttons and links where the text content is not directly within the element tag appear as `get_by_role()` without a `name` attribute

These features and behaviors are candidates for future enhancements based on user needs.

## Development Process

This project was built using a **test-driven development (TDD)** approach with **Claude Code**:

- **Test coverage** — 55 passing tests covering parser, locator selection, code generation, and CLI integration
- **Documentation** — `CLAUDE.md` provides architecture notes and development guidance
- **Plan mode** — Complex implementation tasks used plan mode to design the approach before coding
- **Regression tests** — A bug fix (commit `c73d85b`) refined button and link locator logic; a regression test ensures the fix remains stable

For more details on the development approach and architecture, see `CLAUDE.md`.
