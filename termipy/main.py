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
            case "exit" | "exit 0":
                return False
            case "echo":
                sys.stdout.write(f"{' '.join(args)}\n")
                sys.stdout.flush()
            case "pwd":
                sys.stdout.write(f"{os.getcwd()}\n")
                sys.stdout.flush()
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
                find_file(args[0])
            case "setPyenv":
                handle_setpyenv(args, command)
            case "setRenv":
                handle_setrenv(args, command)
            case "help":
                print("DOCUMENTATION\n")
            case "about":
                if args:
                    get_file_details(args[0])
                else:
                    sys.stdout.write("Error: No file specified for about command.\n")
                    sys.stdout.flush()
            case _:
                try:
                    result = subprocess.run([cmd] + args, capture_output=True, text=True)
                    sys.stdout.write(result.stdout)
                    sys.stdout.flush()
                    sys.stderr.write(result.stderr)
                    sys.stdout.flush()
                except FileNotFoundError:
                    sys.stdout.write(f"{cmd}: command not found\n")
                    sys.stdout.flush()
                except Exception as e:
                    sys.stdout.write(f"Error executing {cmd}: {str(e)}\n")
                    sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"Error processing command: {str(e)}\n")
        sys.stdout.flush()
    return True

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
