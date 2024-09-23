import os
import sys
import subprocess
import readline
from datetime import datetime
from termipy.utils import get_file_details, list_dir, completer
from termipy.env_setup import create_virtual_environment
from termipy.docs import welcome_message, help_message

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
PATHS = os.getenv("PATH").split(":")

def handle_tree(args, command):
    """Handle tree command to list directory structure."""
    level = int(args[0]) if args else 1
    curr_dir = os.getcwd()
    sys.stdout.write(f"{curr_dir}\n")
    list_dir(curr_dir, level, 0)
    sys.stdout.write("\n")

def handle_type(args, command):
    """Handle the type command to check if a command is built-in or from the system."""
    builtins = {"echo", "exit", "cd", "pwd", "clear", "type", "help"}
    command_to_check = args[0] if args else ''
    
    if command_to_check in builtins:
        sys.stdout.write(f"{command_to_check} is a shell builtin\n")
    else:
        for path in PATHS:
            path_to_cmd = os.path.join(path, command_to_check)
            if os.access(path_to_cmd, os.X_OK):
                sys.stdout.write(f"{command_to_check} is {path_to_cmd}\n")
                return
        sys.stdout.write(f"{command_to_check}: not found\n")

def handle_cd(args, command):
    """Handle the cd command to change directories."""
    try:
        new_dir = os.path.expanduser(args[0]) if args and args[0] == "~" else os.path.abspath(args[0])
        os.chdir(new_dir)
    except (IndexError, FileNotFoundError):
        sys.stdout.write(f"{command}: No such file or directory\n")

def handle_input(command):
    """Handle the user input and route to appropriate function."""
    parts = command.split()
    if not parts:
        return True
    
    cmd, *args = parts
    
    match cmd:
        case "exit" | "exit 0":
            return False
        case "echo":
            sys.stdout.write(f"{' '.join(args)}\n")
        case "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        case "cd":
            handle_cd(args, command)
        case "type":
            handle_type(args, command)
        case "clear":
            os.system("clear")
        case "tree":
            handle_tree(args, command)
        case "setenv":
            handle_setenv(args, command)
        case "help":
            pass
        case "about":
            get_file_details(args[0])
        case _:
            try:
                result = subprocess.run([cmd] + args, capture_output=True, text=True)
                sys.stdout.write(result.stdout)
                sys.stderr.write(result.stderr)
            except FileNotFoundError:
                sys.stdout.write(f"{cmd}: command not found\n")

    return True
    

def handle_setenv(args, command):
    """Handle the 'setenv' command to set up a Python environment."""
    python_version = "3.10"
    req_file = None
    project_name = "my-app"

    for i, arg in enumerate(args):
        if arg == "--python" and i + 1 < len(args):
            python_version = args[i + 1]
        elif arg == "--req" and i + 1 < len(args):
            req_file = args[i + 1]
        elif arg == "--name" and i + 1 < len(args):
            project_name = args[i + 1]

    create_virtual_environment(python_version, project_name, req_file)

def input_with_prompt():
    prompt = "@termipy >> "
    sys.stdout.write(prompt)
    sys.stdout.flush()
    user_input = input()  
    return user_input

def main():
    sys.stdout.write(welcome_message)
    sys.stdout.flush()
    while True:
        command = input_with_prompt()
        if command == "help":
            sys.stdout.write(help_message)
            sys.stdout.flush()

        if not handle_input(command):
            break

if __name__ == "__main__":
    main()
