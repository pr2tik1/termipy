### Welcome message
welcome_message = """        
████████╗███████╗██████╗ ███╗   ███╗██╗██████╗ ██╗   ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔══██╗╚██╗ ██╔╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██████╔╝ ╚████╔╝ 
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██╔═══╝   ╚██╔╝  
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║        ██║   
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝        ╚═╝   
                                                        
Welcome to termipy!

Author: Pratik Kumar
Version: 0.1.0
Date: 2024-10-12
Contact: pr2tik1@gmail.com

Supported Commands:
───────────────────────────────────────────────────────
echo <message>        - Prints the message to the terminal
getwd                 - Displays the current working directory
setwd <dir>           - Changes the working directory
typeof <file>         - Shows the type of the file or directory
clr, cls, clear       - Clears the terminal screen
tree <dir>            - Displays the directory tree
create <file>         - Creates a new file
search <file_name>    - Searches for a file by name
setpyenv <env>        - Sets up a Python environment
setrenv <env>         - Sets up an R environment
about <file>          - Displays file details
commands              - Lists all available commands
delete <file/dir>     - Deletes a file or directory
rename <file> <new>   - Renames a file or directory
diskusage             - Shows disk usage information
permissions <file>    - Displays file permissions
exit                  - Exits termipy
───────────────────────────────────────────────────────

Type 'help' for more details on each command.
"""


help_message = """
termipy Command Reference
-------------------------

1. echo <message>       : Prints the specified message to the console.
    Usage: 
    $ echo Hello World
    Output: Hello World

2. exit                 : Exits the shell.
    Usage:
    $ exit
    This will terminate the current session of the shell.

3. setwd <directory>    : Changes the current working directory to the specified directory.
    Usage:
    $ setwd <directory>
    Example: 
    $ setwd /path/to/folder
    Changes the current directory to "/path/to/folder".

4. getwd                : Prints the current working directory (absolute path).
    Usage:
    $ getwd
    Output: Prints the full path of the current directory.

5. clr, cls, clear      : Clears the console screen.
    Usage:
    $ clr
    This command clears all visible text from the shell screen.

6. typeof <command>     : Displays how a command would be interpreted by the shell (builtin, file, etc.).
    Usage:
    $ typeof <command>
    Example: 
    $ typeof ls
    Output: ls is /bin/ls

7. tree <directory>     : Displays the directory structure of the current directory.
    Usage:
    $ tree <directory>
    Example: 
    $ tree /path/to/folder
    Displays the directory structure of "/path/to/folder".

8. create <file>        : Creates a new file with the specified name.
    Usage:
    $ create <file>
    Example:
    $ create new_file.txt
    This will create a file named `new_file.txt`.

9. search <pattern>     : Searches for files or directories matching the specified pattern.
    Usage:
    $ search <pattern>
    Example:
    $ search *.txt
    This will list all `.txt` files in the current directory.

10. setpyenv <env>      : Sets the Python environment.
    Usage:
    $ setpyenv <env>
    Sets the specified Python environment (e.g., virtualenv, conda).

11. setrenv <env>       : Sets the R environment.
    Usage:
    $ setrenv <env>
    Sets the specified R environment.

12. about <file>        : Displays details about the specified file.
    Usage:
    $ about <file>
    Example:
    $ about file.txt
    This will display metadata of `file.txt`.

13. delete <file/dir>   : Deletes the specified file or directory.
    Usage:
    $ delete <file/dir>
    Example:
    $ delete file.txt
    This will remove `file.txt` from the current directory.

14. rename <old_name> <new_name> : Renames a file or directory.
    Usage:
    $ rename <old_name> <new_name>
    Example:
    $ rename old_name.txt new_name.txt
    This will rename `old_name.txt` to `new_name.txt`.

15. diskusage <directory> : Displays disk usage for the specified directory.
    Usage:
    $ diskusage <directory>
    Example:
    $ diskusage /path/to/directory
    This will show how much disk space is used by the specified directory.

16. permissions <file>  : Checks the permissions of the specified file or directory.
    Usage:
    $ permissions <file>
    Example:
    $ permissions my_file.txt
    This will display the permissions for `my_file.txt`.

17. help                : Displays this help message.
    Usage:
    $ help
    Output: Displays the command reference with usage examples.

18. commands            : Lists all built-in commands and executable commands available in the system.
    Usage:
    $ commands
    Output: Displays a list of built-in commands and up to 10 system executables.

"""
