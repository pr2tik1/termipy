import os
import sys
import subprocess
import shutil
from datetime import datetime

def handle_create(args, command):
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

def search(filename):
    """Function to find a file by name."""
    if filename == "-h":
        sys.stdout.write("Usage: search <filename>\nSearch for the specified file in the current directory and subdirectories.\n")
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

def handle_delete(args, command):
    """Delete specified file / folder"""
    if not args:
        return "Please specify file or folder"
    
    target = args[0]
    if not os.path.exists(target):
        sys.stdout.write(f"Error: {target} does not exist.\n")
        return
    
    confirm = input(f"Are you sure you want to delete '{target}'? (y/n): ").lower()
    if confirm != 'y' or confirm != 'Y':
        sys.stdout.write("Deletion canceled.\n")
        return
    try:
        if os.path.isfile(target):
            os.remove(target)
            sys.stdout.write(f"File '{target}' deleted successfully.\n")
        elif os.path.isdir(target):
            if os.listdir(target):
                confirm_non_empty = input(f"Directory '{target}' is not empty. Do you want to delete it and all its contents? (y/n): ").lower()
                if confirm_non_empty != 'y' or confirm_non_empty != 'Y':
                    sys.stdout.write("Deletion of non-empty directory canceled.\n")
                    return
                else:
                    shutil.rmtree(target)
                    sys.stdout.write(f"Non-empty directory '{target}' and its contents deleted successfully.\n")
            else:
                os.rmdir(target)
                sys.stdout.write(f"Empty directory '{target}' deleted successfully.\n")
        else:
            sys.stdout.write(f"Error: {target} is neither a file nor a directory.\n")
    except Exception as e:
        sys.stdout.write(f"Error: Unable to delete {target}: {e}\n")

def handle_rename(args, command):
    """Handle renaming a file or directory."""
    if len(args) != 2:
        sys.stdout.write("Error: Invalid usage of rename. Use: rename <old_name> <new_name>\n")
        return

    old_name, new_name = args
    if not os.path.exists(old_name):
        sys.stdout.write(f"Error: '{old_name}' does not exist.\n")
        return

    if os.path.exists(new_name):
        sys.stdout.write(f"Error: A file or directory with the name '{new_name}' already exists.\n")
        return

    try:
        os.rename(old_name, new_name)
        sys.stdout.write(f"'{old_name}' has been successfully renamed to '{new_name}'.\n")
    except Exception as e:
        sys.stdout.write(f"Error renaming '{old_name}' to '{new_name}': {str(e)}\n")

def check_permissions(args):
    """Check and display the permissions of the specified file or directory."""
    if len(args) != 1:
        sys.stdout.write("Error: Invalid usage of permissions. Use: permissions <file>\n")
        return

    file_path = args[0]

    if not os.path.exists(file_path):
        sys.stdout.write(f"Error: '{file_path}' does not exist.\n")
        return

    try:
        permissions = os.stat(file_path)
        file_mode = permissions.st_mode
        is_directory = 'd' if os.path.isdir(file_path) else '-'
        owner_permissions = (
            'r' if file_mode & os.R_OK else '-',
            'w' if file_mode & os.W_OK else '-',
            'x' if file_mode & os.X_OK else '-'
        )

        sys.stdout.write(f"Permissions for '{file_path}':\n")
        sys.stdout.write(f"  Type        : {'Directory' if is_directory == 'd' else 'File'}\n")
        sys.stdout.write(f"  Readable    : {'Yes' if os.access(file_path, os.R_OK) else 'No'}\n")
        sys.stdout.write(f"  Writable    : {'Yes' if os.access(file_path, os.W_OK) else 'No'}\n")
        sys.stdout.write(f"  Executable  : {'Yes' if os.access(file_path, os.X_OK) else 'No'}\n")
        sys.stdout.write(f"  Owner's Permissions: {''.join(owner_permissions)}\n")

    except Exception as e:
        sys.stdout.write(f"Error checking permissions for '{file_path}': {str(e)}\n")
