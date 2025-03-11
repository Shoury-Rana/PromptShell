import re

def clean_command(raw_command):
    """Extract command from various response formats"""
    # First remove any special tokens
    # cleaned = re.sub(r' ', '', raw_command)
    
    # Then try quoted command
    quoted_match = re.search(r'"([^"]+)"', raw_command)
    if quoted_match:
        return quoted_match.group(1).strip()
    
    # Then code block format
    code_match = re.search(r'```(?:bash|cmd|powershell)?\n(.*?)\n```', raw_command, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
     
    # Finally clean any remaining special characters
    return re.sub(r'^[\'"`]|[\'"`]$', '', raw_command).strip()