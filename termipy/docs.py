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
Date: 2024-09-22
Contact: pr2tik1@gmail.com
\n"""


### Documentation
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

5. clr                  : Clears the console screen.
    Usage:
    $ clr
    This command clears all visible text from the shell screen.

6. typeof <command>     : Displays how a command would be interpreted by the shell (builtin, file, etc.).
    Usage:
    $ typeof <command>
    Example: 
    $ typeof ls
    Output: ls is /bin/ls

7. tree <level number>  : Displays the directory structure of the current directory, up to a specified depth level.
    Usage:
    $ tree <level>
    Example: 
    $ tree 2
    This will display the directory structure up to two levels deep.

8. makedir <directory>  : Creates a new directory.
    Usage:
    $ makedir <directory>
    Example:
    $ makedir new_folder
    This will create a directory named `new_folder` in the current directory.

9. delete <file>        : Deletes the specified file.
    Usage:
    $ delete <file>
    Example:
    $ delete old_file.txt
    This will remove `old_file.txt` from the current directory.

10. search <pattern>     : Searches for files or directories matching the specified pattern.
    Usage:
    $ search <pattern>
    Example:
    $ search *.txt
    This will list all `.txt` files in the current directory.

11. create <file>        : Creates a new file with the specified name.
    Usage:
    $ create <file>
    Example:
    $ create new_file.txt
    This will create a file named `new_file.txt`.

12. view <file>          : Displays the contents of the specified file.
    Usage:
    $ view <file>
    Example:
    $ view existing_file.txt
    This will display the contents of `existing_file.txt`.

13. rename <old_name> <new_name> : Renames a file or directory.
    Usage:
    $ rename <old_name> <new_name>
    Example:
    $ rename old_name.txt new_name.txt
    This will rename `old_name.txt` to `new_name.txt`.

14. diskusage <directory> : Displays disk usage for the specified directory.
    Usage:
    $ diskusage <directory>
    Example:
    $ diskusage /path/to/directory
    This will show how much disk space is used by the specified directory.

15. permissions <file>     : Checks the permissions of the specified file or directory.
    Usage:
    $ permissions <file>
    Example:
    $ permissions my_file.txt
    This will display the permissions for `my_file.txt`.

16. help                : Displays this help message.
    Usage:
    $ help
    Output: Displays the command reference with usage examples.

17. commands            : Lists all built-in commands and executable commands available in the system, limited to 10 displayed executables.
    Usage:
    $ commands
    Output: Displays a list of built-in commands followed by up to 10 executable commands. If there are more than 10, it will indicate how many more are available.

"""