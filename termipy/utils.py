import os
import sys
import subprocess
from datetime import datetime

def handle_mkdir(args, command):
    """Create a directory if it does not exist."""
    if "-h" in args:
        sys.stdout.write("Usage: mkdir <directory_name>\nCreate a directory with the specified name.\n")
        return
    
    if not args:
        sys.stdout.write("Error: No directory name provided.\n")
        return

    directory_name = args[0]
    try:
        os.makedirs(directory_name, exist_ok=True)
        sys.stdout.write(f"Directory '{directory_name}' created successfully or already exists.\n")
    except Exception as e:
        sys.stdout.write(f"Error creating directory '{directory_name}': {str(e)}\n")


def handle_tree(args, command):
    """Handle tree command to list directory structure."""
    show_hidden = False
    level = 1

    if "-h" in args:
        sys.stdout.write("Usage: tree [-h] [level]\nList the directory structure. Use -h to show hidden files.\n")
        return

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
                    list_dir(full_path, max_level, curr_level + 1, show_hidden)
                else:
                    sys.stdout.write(f"\n{'  ' * curr_level}{prefix}{item}")
        except PermissionError:
            sys.stdout.write(f"{curr_dir}: Permission denied\n")


def handle_type(args, command):
    """Handle the type command to check if a command is built-in or from the system."""
    if "-h" in args:
        sys.stdout.write("Usage: type <command>\nCheck if the specified command is built-in or system command.\n")
        return
    
    command_to_check = args[0] if args else ''
    builtins = {"echo", "exit", "cd", "pwd", "clear", "type", "help"}
    PATHS = os.getenv("PATH").split(":")
    
    if command_to_check in builtins:
        sys.stdout.write(f"{command_to_check} is a shell builtin\n")
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
    if "-h" in args:
        sys.stdout.write("Usage: cd <directory_name>\nChange the current directory to the specified directory.\n")
        return

    try:
        new_dir = os.path.expanduser(args[0]) if args and args[0] == "~" else os.path.abspath(args[0])
        os.chdir(new_dir)
    except IndexError:
        sys.stdout.write("cd: No directory specified.\n")
    except FileNotFoundError:
        sys.stdout.write(f"{command}: No such file or directory\n")
    except PermissionError:
        sys.stdout.write(f"{command}: Permission denied to access {new_dir}\n")


def get_file_details(path):
    """Retrieve and display details about a specified file."""
    if "-h" in path:
        sys.stdout.write("Usage: get_file_details <file_path>\nRetrieve details about the specified file.\n")
        return
    
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
    except FileNotFoundError:
        sys.stdout.write(f"{path} does not exist.\n")
    except PermissionError:
        sys.stdout.write(f"Permission denied to access {path}\n")


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
        return None

def find_file(filename):
    """Function to find a file by name."""
    if filename == "-h":
        sys.stdout.write("Usage: find_file <filename>\nSearch for the specified file in the current directory and subdirectories.\n")
        return
    
    found_files = []
    sys.stdout.write("Searching in current directory...\n")
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            found_files.append(os.path.join(root, filename))

    if found_files:
        sys.stdout.write("Found file(s):\n")
        for file in found_files:
            sys.stdout.write(f"{file}\n")
    else:
        sys.stdout.write(f"No files found with the name: {filename}\n")

def list_builtins_and_executables():
    """List all built-in commands and executable commands."""
    builtins = {"echo", "exit", "cd", "pwd", "clear", "type", "help", "mkdir", "tree", "ff", "setPyenv", "setRenv", "about"}
    sys.stdout.write("Built-in Commands:\n")
    for cmd in sorted(builtins):
        sys.stdout.write(f"  - {cmd}\n")
    
    sys.stdout.write("\nExecutable Commands:\n")
    PATHS = os.getenv("PATH").split(":")
    executables = set()

    for path in PATHS:
        if os.path.isdir(path):
            try:
                items = os.listdir(path)
                for item in items:
                    if os.access(os.path.join(path, item), os.X_OK):
                        executables.add(item)
            except Exception as e:
                sys.stdout.write(f"Error accessing {path}: {e}\n")

    executables_list = sorted(executables)
    for cmd in executables_list[:10]:
        sys.stdout.write(f"  - {cmd}\n")
    
    if len(executables_list) > 10:
        sys.stdout.write(f"  ... {len(executables_list) - 10} more executable commands\n")
    