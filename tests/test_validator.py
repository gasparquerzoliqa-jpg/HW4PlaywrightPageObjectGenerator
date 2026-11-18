import pytest
from pom_generator.validator import validate_and_normalize_names


class TestValidatorConversions:
    def test_converts_to_snake_case(self):
        names = ["Submit Button"]
        result = validate_and_normalize_names(names)
        assert result[0] == "submit_button"

    def test_converts_camel_case_to_snake_case(self):
        names = ["submitButton", "loginForm"]
        result = validate_and_normalize_names(names)
        assert result[0] == "submit_button"
        assert result[1] == "login_form"

    def test_sanitizes_special_chars(self):
        names = ["Button #1", "Form$Name"]
        result = validate_and_normalize_names(names)
        assert result[0] == "button_1"
        assert result[1] == "form_name"

    def test_generates_unique_names_with_duplicates(self):
        names = ["submit", "submit", "submit"]
        result = validate_and_normalize_names(names)
        assert result == ["submit", "submit_2", "submit_3"]

    def test_generates_unique_names_mixed(self):
        names = ["login", "Login", "login"]
        result = validate_and_normalize_names(names)
        assert result[0] == "login"
        assert result[1] == "login_2"
        assert result[2] == "login_3"

    def test_preserves_order(self):
        names = ["button_a", "button_a", "button_b"]
        result = validate_and_normalize_names(names)
        assert result[0] == "button_a"
        assert result[1] == "button_a_2"
        assert result[2] == "button_b"

    def test_validates_python_identifier(self):
        names = ["valid_name", "_leading_underscore", "name123"]
        result = validate_and_normalize_names(names)
        assert all(name.isidentifier() for name in result)

    def test_handles_numbers(self):
        names = ["Button 1", "Input 2"]
        result = validate_and_normalize_names(names)
        assert result[0] == "button_1"
        assert result[1] == "input_2"

    def test_empty_list(self):
        result = validate_and_normalize_names([])
        assert result == []

    def test_single_name(self):
        names = ["SingleElement"]
        result = validate_and_normalize_names(names)
        assert result[0] == "single_element"
