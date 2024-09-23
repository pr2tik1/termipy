import os
import sys
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
            case "getwd":
                sys.stdout.write(f"{os.getcwd()}\n")
            case "setwd":
                handle_cd(args, command)
            case "typeof":
                handle_type(args, command)
            case "clr" | "cls" | "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
            case "tree":
                handle_tree(args, command)
            case "makedir":
                handle_mkdir(args, command)
            case "ff":
                if args:
                    find_file(args[0])
                else:
                    sys.stdout.write("Error: No filename specified for find_file command.\n")
            case "setpyenv":
                handle_setpyenv(args, command)
            case "setrenv":
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
            case "delete":
                handle_delete(args, command)
            case "search":
                handle_search(args, command)
            case "create":
                handle_create(args, command)
            case "view":
                handle_view(args, command)
            case "rename":
                handle_rename(args, command)
            case "diskusage":
                display_disk_usage(args)
            case "permissions":
                check_permissions(args)
            case _:
                sys.stdout.write(f"{cmd}: command not found\n")
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