import os
import sys
import subprocess
import readline
from datetime import datetime
from termipy.utils import *
from termipy.env_setup import handle_setpyenv, handle_setrenv
from termipy.docs import welcome_message, help_message

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def handle_input(command):
    """Handle the user input and route to appropriate function."""
    parts = command.split()
    if not parts:
        return True
    cmd, *args = parts
    try:
        match cmd:
            case "exit":
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
            case "mkdir":
                handle_mkdir(args, command)
            case "ff":
                if args:
                    find_file(args[0])
                else:
                    sys.stdout.write("Error: No filename specified for find_file command.\n")
            case "setPyenv":
                handle_setpyenv(args, command)
            case "setRenv":
                handle_setrenv(args, command)
            case "help":
                sys.stdout.write(help_message)
            case "about":
                if args:
                    get_file_details(args[0])
                else:
                    sys.stdout.write("Error: No file specified for about command.\n")
            case "commands":
                list_builtins_and_executables()
            case _:
                try:
                    result = subprocess.run([cmd] + args, capture_output=True, text=True)
                    sys.stdout.write(result.stdout)
                    sys.stderr.write(result.stderr)
                except FileNotFoundError:
                    sys.stdout.write(f"{cmd}: command not found\n")
                except Exception as e:
                    sys.stdout.write(f"Error executing {cmd}: {str(e)}\n")
    except Exception as e:
        sys.stdout.write(f"Error processing command: {str(e)}\n")
    return True

def main():
    sys.stdout.write(welcome_message)
    sys.stdout.flush()
    prompt = "@termipy >> "
    
    while True:
        command = input(prompt)
        if not handle_input(command):
            break

if __name__ == "__main__":
    main()
