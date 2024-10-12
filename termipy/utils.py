import os
import sys
import shutil
import subprocess
from datetime import datetime

def list_builtins_and_executables():
    """List all built-in commands and executable commands."""
    builtins = {
        "echo", "exit", "setwd", "getwd", "clr", "typeof", "tree", "create", 
        "search", "setpyenv", "setrenv", "help", "about", "commands", "delete", 
        "rename", "diskusage", "permissions"
    }
    
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

def display_disk_usage(args):
    """Display disk usage for the specified directory."""
    if len(args) != 1:
        sys.stdout.write("Error: Invalid usage of diskusage. Use: diskusage <directory>\n")
        return
    directory = args[0]
    if not os.path.isdir(directory):
        sys.stdout.write(f"Error: '{directory}' is not a valid directory.\n")
        return

    try:
        total, used, free = shutil.disk_usage(directory)
        total_gb = total / (2**30)
        used_gb = used / (2**30)
        free_gb = free / (2**30)

        sys.stdout.write(f"Disk Usage for '{directory}':\n")
        sys.stdout.write(f"  Total space : {total_gb:.2f} GB\n")
        sys.stdout.write(f"  Used space  : {used_gb:.2f} GB\n")
        sys.stdout.write(f"  Free space  : {free_gb:.2f} GB\n")

    except Exception as e:
        sys.stdout.write(f"Error retrieving disk usage for '{directory}': {str(e)}\n")
