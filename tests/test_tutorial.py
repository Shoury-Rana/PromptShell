from unittest.mock import patch, MagicMock
from io import StringIO
from promptshell.main import main

def test_tutorial_command():
    """Test that entering --tutorial in the REPL launches the tutorial and prints the welcome message."""
    with patch('builtins.input', side_effect=['--tutorial', 'exit']), \
         patch('sys.stdout', new=StringIO()) as fake_out, \
         patch('questionary.confirm', return_value=MagicMock(ask=lambda: True)):
        main()
        output = fake_out.getvalue()
        assert "Welcome to the interactive tutorial for PromptShell!" in output 