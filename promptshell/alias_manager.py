import json
import os
import re
from datetime import datetime
from .setup import CONFIG_DIR

ALIAS_FILE = os.path.join(CONFIG_DIR, "aliases.json")

class AliasManager:
    def __init__(self):
        self.aliases = {}
        self.blacklist = ["rm -rf /", "chmod -R 777 /", ":(){:|:&};:", "mkfs", "dd if=/dev/random"]
        self.load_aliases()
    
    def load_aliases(self):
        if os.path.exists(ALIAS_FILE):
            try:
                with open(ALIAS_FILE, 'r') as f:
                    data = json.load(f)
                    self.aliases = data.get('aliases', {})
            except (json.JSONDecodeError, IOError):
                self.aliases = {}
    
    def save_aliases(self):
        with open(ALIAS_FILE, 'w') as f:
            json.dump({'aliases': self.aliases}, f, indent=2)
    
    def validate_alias_name(self, name):
        return re.match(r'^[a-zA-Z_]\w*$', name) is not None
    
    def validate_command(self, command):
        for dangerous in self.blacklist:
            if dangerous in command:
                return False
        return True
    
    def add_alias(self, name, command, description=""):
        if not self.validate_alias_name(name):
            return False, "Invalid alias name. Must be alphanumeric with underscores"
        
        if not self.validate_command(command):
            return False, "Command contains dangerous patterns"
        
        if name in self.aliases:
            return False, "Alias already exists"
        
        self.aliases[name] = {
            'command': command,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.save_aliases()
        return True, f"Alias '{name}' added"
    
    def remove_alias(self, name):
        if name not in self.aliases:
            return False, "Alias not found"
        
        del self.aliases[name]
        self.save_aliases()
        return True, f"Alias '{name}' removed"
    
    def list_aliases(self, name=None):
        if name:
            return self.aliases.get(name, None)
        return self.aliases
    
    def import_aliases(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for name, alias_data in data.get('aliases', {}).items():
                    if self.validate_alias_name(name) and self.validate_command(alias_data.get('command', '')):
                        self.aliases[name] = alias_data
            self.save_aliases()
            return True, "Aliases imported successfully"
        except Exception as e:
            return False, f"Import failed: {str(e)}"
    
    def export_aliases(self, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump({'aliases': self.aliases}, f, indent=2)
            return True, "Aliases exported successfully"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def expand_alias(self, input_command):
        parts = input_command.strip().split(maxsplit=1)
        if not parts:
            return input_command
        
        alias_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        if alias_name in self.aliases:
            base_command = self.aliases[alias_name]['command']
            return f"{base_command} {args}".strip()
        return input_command