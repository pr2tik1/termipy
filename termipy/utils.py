import os
import sys
import subprocess
from datetime import datetime

def get_file_details(path):
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

def list_dir(curr_dir, max_level, curr_level):
    if curr_level < max_level:
        try:
            items = os.listdir(curr_dir)
            for item in items:
                full_path = os.path.join(curr_dir, item)
                if os.path.isdir(full_path):
                    sys.stdout.write(f"\n{'  ' * curr_level}├── {item}")
                    list_dir(full_path, max_level, curr_level + 1)
                else:
                    sys.stdout.write(f"\n{'  ' * curr_level}├── {item}")
        except PermissionError:
            sys.stdout.write(f"{curr_dir}: Permission denied\n")

def completer(text, state):
    options = [x for x in os.listdir(os.getcwd()) if x.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None