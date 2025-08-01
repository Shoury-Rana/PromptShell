import pytest
from promptshell.format_utils import text_theme, reset_format, get_current_os

def test_text_theme():
    # Test foreground color
    assert text_theme('error') == "\033[0m\033[31m"
    # Test bold style
    assert text_theme('prompt', bold=True) == "\033[0m\033[1m\033[32m"
    # Test background color
    assert text_theme('info', bg='white') == "\033[0m\033[36m\033[47m"

def test_reset_format():
    assert reset_format() == "\033[0m"

@pytest.mark.parametrize("platform_system, expected_os", [
    ("Linux", "linux"),
    ("Windows", "windows"),
    ("Darwin", "macos"),
])
def test_get_current_os(mocker, platform_system, expected_os):
    mocker.patch('platform.system', return_value=platform_system)
    assert get_current_os() == expected_os
