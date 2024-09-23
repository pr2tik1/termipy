import os
import sys
import subprocess
from datetime import datetime

def handle_tree(args, command):
    """Handle tree command to list directory structure."""
    show_hidden = False
    level = 1

    for arg in args:
        if arg.startswith('-h'):
            show_hidden = True
        else:
            try:
                level = int(arg)
            except ValueError:
                sys.stdout.write("Invalid level number specified. Defaulting to 1.\n")
                level = 1

    try:
        curr_dir = os.getcwd()
        sys.stdout.write(f"{curr_dir}\n")
        list_dir(curr_dir, level, 0, show_hidden)
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"Error: {str(e)}\n")

def list_dir(curr_dir, max_level, curr_level, show_hidden):
    """List directory contents, optionally showing hidden files."""
    if curr_level < max_level:
        try:
            items = os.listdir(curr_dir)
            for index, item in enumerate(items):
                if not show_hidden and item.startswith('.'):
                    continue  # Skip hidden files if not showing them
                full_path = os.path.join(curr_dir, item)
                is_last = index == len(items) - 1
                prefix = "└── " if is_last else "├── "
                if os.path.isdir(full_path):
                    sys.stdout.write(f"\n{'  ' * curr_level}{prefix}{item}")
                    sys.stdout.flush()
                    list_dir(full_path, max_level, curr_level + 1, show_hidden)
                else:
                    sys.stdout.write(f"\n{'  ' * curr_level}{prefix}{item}")
        except PermissionError:
            sys.stdout.write(f"{curr_dir}: Permission denied\n")
            sys.stdout.flush()


def handle_type(args, command):
    """Handle the type command to check if a command is built-in or from the system."""
    builtins = {"echo", "exit", "cd", "pwd", "clear", "type", "help"}
    command_to_check = args[0] if args else ''
    PATHS = os.getenv("PATH").split(":")    
    if command_to_check in builtins:
        sys.stdout.write(f"{command_to_check} is a shell builtin\n")
        sys.stdout.flush()
    else:
        found = False
        for path in PATHS:
            try:
                path_to_cmd = os.path.join(path, command_to_check)
                if os.access(path_to_cmd, os.X_OK):
                    sys.stdout.write(f"{command_to_check} is {path_to_cmd}\n")
                    found = True
                    break
            except Exception as e:
                sys.stdout.write(f"Error checking command: {e}\n")
        
        if not found:
            sys.stdout.write(f"{command_to_check}: not found\n")

def handle_cd(args, command):
    """Handle the cd command to change directories."""
    try:
        new_dir = os.path.expanduser(args[0]) if args and args[0] == "~" else os.path.abspath(args[0])
        os.chdir(new_dir)
    except IndexError:
        sys.stdout.write("cd: No directory specified.\n")
        sys.stdout.flush()
    except FileNotFoundError:
        sys.stdout.write(f"{command}: No such file or directory\n")
        sys.stdout.flush()
    except PermissionError:
        sys.stdout.write(f"{command}: Permission denied to access {new_dir}\n")
        sys.stdout.flush()

def get_file_details(path):
    """Retrieve and display details about a specified file."""
    try:
        size = os.path.getsize(path)
        abs_path = os.path.abspath(path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(path))
        is_directory = os.path.isdir(path)
        sys.stdout.write(f"{'-'*40}\n")
        sys.stdout.write(f"Absolute Path: {abs_path}\n")
        sys.stdout.write(f"Size: {size} bytes\n")
        sys.stdout.write(f"Last Modified: {mod_time}\n")
        sys.stdout.write(f"Is Directory: {is_directory}\n")
        sys.stdout.write(f"{'-'*40}\n")
        sys.stdout.flush()
    except FileNotFoundError:
        sys.stdout.write(f"{path} does not exist.\n")
        sys.stdout.flush()
    except PermissionError:
        sys.stdout.write(f"Permission denied to access {path}\n")
        sys.stdout.flush()

def completer(text, state):
    """Provide autocompletion for commands based on current directory contents."""
    try:
        options = [x for x in os.listdir(os.getcwd()) if x.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None
    except Exception as e:
        sys.stdout.write(f"Error accessing current directory: {e}\n")
        sys.stdout.flush()
        return None

def find_file(filename):
    """Function to find a file by name."""
    found_files = []
    sys.stdout.write("Searching in current directory...\n")
    sys.stdout.flush()
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            found_files.append(os.path.join(root, filename))

    if found_files:
        sys.stdout.write("Found file(s):\n")
        sys.stdout.flush()
        for file in found_files:
            sys.stdout.write(f"{file}\n")
        sys.stdout.flush()
    else:
        sys.stdout.write(f"No files found with the name: {filename}\n")
        sys.stdout.flush()
