import os
import sys
import subprocess

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

def handle_tree(args, command):    
    level = 1
    if args:
        level = int(args[0])
    curr_dir = os.getcwd()
    sys.stdout.write(curr_dir)
    list_dir(curr_dir, level, 0)
    sys.stdout.write("\n")

def handle_type(args, command):
    builtins = ["echo", "exit", "cd", "pwd", "clear", "type", "help"]
    paths = os.getenv("PATH").split(":")
    command_to_check = args[0] if args else ''
    path_to_cmd = ''

    if command_to_check in builtins:
        sys.stdout.write(f"{command_to_check} is a shell builtin\n")
    else:
        for path in paths:
            if os.path.isfile(f"{path}/{command_to_check}"):
                path_to_cmd = f"{path}/{command_to_check}"
        if path_to_cmd:
            sys.stdout.write(f"{command_to_check} is {path_to_cmd}\n")
        else:
            sys.stdout.write(f"{command_to_check}: not found\n")

def handle_cd(args, command):
    curr_dir = os.getcwd()
    try:
        if args[0] == "~":
            os.chdir(os.path.expanduser("~"))
        else:
            os.chdir(os.path.join(curr_dir, args[0]))
    except FileNotFoundError:
        sys.stdout.write(f"{command}: No such file or directory\n")

def handle_input(command):
    parts = command.split()
    cmd = parts[0]
    args = parts[1:]

    match cmd:
        case "exit" | "exit 0":
            return False
        case "echo":
            sys.stdout.write(f"{''.join(args)}\n")
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
        case "help":
            pass
        case _:
            try:
                result = subprocess.run([cmd] + args, capture_output=True, text=True)
                sys.stdout.write(result.stdout)
                sys.stderr.write(result.stderr)
            except FileNotFoundError:
                sys.stdout.write(f"{cmd}: command not found\n")

    return True

def main():
    welcome_message = """        
███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗
██╔════╝██║  ██║██╔════╝██║     ██║     ╚══███╔╝
███████╗███████║█████╗  ██║     ██║       ███╔╝ 
╚════██║██╔══██║██╔══╝  ██║     ██║      ███╔╝  
███████║██║  ██║███████╗███████╗███████╗███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
Welcome to Shellz!

1. echo <message>       - Prints the message to the console.
2. exit                 - Exits the shell.
3. cd <directory>       - Changes the current directory.
4. pwd                  - Prints the current working directory.
5. clear                - Clears the console screen.
6. type <command>       - Displays how a command would be interpreted.
7. tree <level number>  - Displays the directory structure up to a specified level.
8. ls                   - List files / folders.
9. help                 - Display documentation.

Author: Pratik Kumar
Version: 1.0
Date: 2024-09-22
Contact: pr2tik1@gmail.com
    \n"""
    sys.stdout.write(welcome_message)
    sys.stdout.flush()
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        if command == "help":
            sys.stdout.write(welcome_message)
            sys.stdout.flush()

        if not handle_input(command):
            break

if __name__ == "__main__":
    main()

