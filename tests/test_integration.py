import pytest
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch
import ast
import generate

# Adjust path to import generate module
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "output"


class TestCLIIntegration:
    def test_cli_generates_file_in_output(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file)])

        generated_files = list(output_dir.glob("*.py"))
        assert len(generated_files) > 0

    def test_cli_with_custom_class_name(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file), '--class-name', 'LoginForm'])

        login_form_file = output_dir / "LoginForm.py"
        assert login_form_file.exists()

    def test_cli_with_default_class_name(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file)])

        pageobject_file = output_dir / "PageObject.py"
        assert pageobject_file.exists()

    def test_cli_reads_html_file(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        assert html_file.exists()

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file)])

        generated_files = list(output_dir.glob("*.py"))
        assert len(generated_files) > 0

    def test_cli_prints_error_for_empty_html(self, fixtures_dir, output_dir, capsys):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "empty.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            try:
                generate.main([str(html_file)])
            except SystemExit:
                pass

        captured = capsys.readouterr()
        assert "No interactive elements found" in captured.out or "No interactive elements found" in captured.err

    def test_generated_file_is_valid_python(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file), '--class-name', 'TestPage'])

        generated_file = output_dir / "TestPage.py"
        assert generated_file.exists()

        code = generated_file.read_text()
        try:
            ast.parse(code)
        except SyntaxError as e:
            pytest.fail(f"Generated file has syntax errors:\n{e}")

    def test_generated_file_contains_class_definition(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file), '--class-name', 'FormPage'])

        generated_file = output_dir / "FormPage.py"
        code = generated_file.read_text()
        assert 'class FormPage' in code

    def test_generated_file_imports_playwright(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file)])

        generated_file = list(output_dir.glob("*.py"))[0]
        code = generated_file.read_text()
        assert 'from playwright' in code or 'import' in code

    def test_end_to_end_simple_form(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "simple_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file), '--class-name', 'LoginPage'])

        generated_file = output_dir / "LoginPage.py"
        assert generated_file.exists()

        code = generated_file.read_text()
        assert 'class LoginPage' in code
        assert 'def __init__' in code
        assert 'self.' in code
        assert 'page.get_by' in code or 'page.locator' in code

    def test_end_to_end_complex_form(self, fixtures_dir, output_dir):
        output_dir.mkdir(exist_ok=True)
        html_file = fixtures_dir / "complex_form.html"

        with patch.object(generate, 'OUTPUT_DIR', output_dir):
            generate.main([str(html_file), '--class-name', 'RegistrationPage'])

        generated_file = output_dir / "RegistrationPage.py"
        assert generated_file.exists()

        code = generated_file.read_text()
        assert 'class RegistrationPage' in code
        try:
            ast.parse(code)
        except SyntaxError:
            pytest.fail(f"Generated code is not valid Python:\n{code}")
