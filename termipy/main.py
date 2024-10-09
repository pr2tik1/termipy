import os
import sys
import readline
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
        if cmd == "exit":
            return False
        elif cmd == "echo":
            sys.stdout.write(f"{' '.join(args)}\n")
        elif cmd == "getwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        elif cmd == "setwd":
            handle_cd(args, command)
        elif cmd == "typeof":
            handle_type(args, command)
        elif cmd in ["clr", "cls", "clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd == "tree":
            handle_tree(args, command)
        elif cmd == "makedir":
            handle_mkdir(args, command)
        elif cmd == "ff":
            if args:
                find_file(args[0])
            else:
                sys.stdout.write("Error: No filename specified for find_file command.\n")
        elif cmd == "setpyenv":
            handle_setpyenv(args, command)
        elif cmd == "setrenv":
            handle_setrenv(args, command)
        elif cmd == "help":
            sys.stdout.write(help_message)
        elif cmd == "about":
            if args:
                get_file_details(args[0])
            else:
                sys.stdout.write("Error: No file specified for about command.\n")
        elif cmd == "commands":
            list_builtins_and_executables()
        elif cmd == "delete":
            handle_delete(args, command)
        elif cmd == "search":
            handle_search(args, command)
        elif cmd == "create":
            handle_create(args, command)
        elif cmd == "view":
            handle_view(args, command)
        elif cmd == "rename":
            handle_rename(args, command)
        elif cmd == "diskusage":
            display_disk_usage(args)
        elif cmd == "permissions":
            check_permissions(args)
        else:
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
