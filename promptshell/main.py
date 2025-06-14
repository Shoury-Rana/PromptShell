from .ai_terminal_assistant import AITerminalAssistant
from .readline_setup import setup_readline
import platform
import os
from .ansi_support import enable_ansi_support
from .format_utils import format_text, reset_format, get_terminal_size
from .setup import setup_wizard, load_config, get_active_model
import shlex
from .alias_manager import AliasManager

def main():
    config = load_config()
    if not config:
        print("First-time setup required!")
        setup_wizard()
        config = load_config()

    enable_ansi_support()
    setup_readline()
    model_name = get_active_model()

    assistant = AITerminalAssistant(config=config, model_name=model_name)

    print(f"""\n{format_text('green', bold=True)}Welcome to the AI-Powered Terminal Assistant!
Active provider: ({model_name} - {platform.system()})
Type '--help' for assistance and '--config' for settings.{reset_format()}""")
    
    while True:
        try:
            columns, _ = get_terminal_size()
            prompt = f"\n{format_text('green', bold=True)}{os.getcwd()}$ {reset_format()}"
            user_input = input(prompt)

            if len(prompt) + len(user_input) > columns:
                print()  # Move to the next line if input is too long

            if user_input.lower() == 'quit':
                print(format_text('red', bold=True) + "\nTerminating..." + reset_format())
                break

            if user_input.lower() == "--config":
                setup_wizard()
                config = load_config()
                model_name = get_active_model()
                assistant = AITerminalAssistant(config=config, model_name=model_name)
                print(f"{format_text('yellow', bold=True)}Configuration updated!{reset_format()}")
                continue

            if user_input.lower() == "--help":
                print(f"""{format_text('blue')}- You can use natural language queries or standard shell commands.
- Start your input with '!' to execute a command directly without processing.
- Start or end your input with '?' to ask a question.
- Tab completion for files and folders is enabled.
- Use 'Ctrl + c' or type 'quit' to quit the assistant.
- Type 'clear' to clear the terminal.{reset_format()}""")
                continue

            if user_input.lower().startswith("alias "):
                result = handle_alias_command(user_input, assistant.alias_manager)
                print(result)
                continue

            result = assistant.execute_command(user_input)
            print(result)

        except KeyboardInterrupt:
            print(format_text('red', bold=True) + "\nTerminating..." + reset_format())
            break

def handle_alias_command(command: str, alias_manager: AliasManager) -> str:
    try:
        parts = shlex.split(command)
        if len(parts) < 2:
            return "Usage: alias [add|remove|list|import|export|help]"
        
        subcommand = parts[1].lower()
        
        if subcommand == "add" and len(parts) >= 4:
            name = parts[2]
            cmd = " ".join(parts[3:])
            _, message = alias_manager.add_alias(name, cmd)
            return message
        
        elif subcommand == "remove" and len(parts) >= 3:
            _, message = alias_manager.remove_alias(parts[2])
            return message
        
        elif subcommand == "list":
            if len(parts) >= 3:
                alias = alias_manager.list_aliases(parts[2])
                if alias:
                    return f"{parts[2]}: {alias['command']}\nDescription: {alias.get('description', '')}"
                return "Alias not found"
            aliases = alias_manager.list_aliases()
            return "\n".join([f"{name}: {data['command']}" for name, data in aliases.items()])
        
        elif subcommand == "import" and len(parts) >= 3:
            _, message = alias_manager.import_aliases(parts[2])
            return message
        
        elif subcommand == "export" and len(parts) >= 3:
            _, message = alias_manager.export_aliases(parts[2])
            return message
        
        elif subcommand == "help":
            return (
                "Alias Management Commands:\n"
                "  alias add <name> \"<command>\" - Add new alias\n"
                "  alias remove <name> - Remove alias\n"
                "  alias list [name] - List all aliases or show details\n"
                "  alias import <file> - Import aliases from JSON file\n"
                "  alias export <file> - Export aliases to JSON file\n"
                "  alias help - Show this help"
            )
        
        return "Invalid alias command"
    except Exception as e:
        return f"Error processing alias command: {str(e)}"

if __name__ == "__main__":
    main()