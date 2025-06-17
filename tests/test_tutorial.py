
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from promptshell.main import main

def test_tutorial_flag():
    """Test that --tutorial flag launches the tutorial and prints the welcome message."""
    with patch('sys.argv', ['promptshell', '--tutorial']), \
         patch('sys.stdout', new=StringIO()) as fake_out, \
         patch('builtins.input', side_effect=['exit']), \
         patch('questionary.confirm', return_value=MagicMock(ask=lambda: True)):
        main()
        output = fake_out.getvalue()
        assert "Welcome to the interactive tutorial for PromptShell!" in output 