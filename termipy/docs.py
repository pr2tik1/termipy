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
Version: 1.0
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

3. cd <directory>       : Changes the current working directory to the specified directory.
    Usage:
    $ cd <directory>
    Example: 
    $ cd /path/to/folder
    Changes the current directory to "/path/to/folder".

4. pwd                  : Prints the current working directory (absolute path).
    Usage:
    $ pwd
    Output: Prints the full path of the current directory.

5. clear                : Clears the console screen.
    Usage:
    $ clear
    This command clears all visible text from the shell screen.

6. type <command>       : Displays how a command would be interpreted by the shell (builtin, file, etc.).
    Usage:
    $ type <command>
    Example: 
    $ type ls
    Output: ls is /bin/ls
    This tells you that `ls` is a binary file located at `/bin/ls`.

7. tree <level number>  : Displays the directory structure of the current directory, up to a specified depth level.
    Usage:
    $ tree <level>
    Example: 
    $ tree 2
    This will display the directory structure up to two levels deep.

8. ls                   : Lists files and folders in the current directory.
    Usage:
    $ ls
    Output: Displays the names of the files and directories in the current working directory.

9. setPyenv --python <version> --req <file> --name <project> : Sets up a new Python environment with a specified Python version, installs dependencies, and creates a project directory.
    Usage:
    $ setPyenv --python <version> --req <requirements.txt> --name <project-name>
    Example:
    $ setPyenv --python 3.10 --req requirements.txt --name my-flask-app
    This will:
    - Create a project directory named `my-flask-app`.
    - Set up a virtual environment using Python version 3.10 inside the project directory.
    - Install the Python dependencies listed in `requirements.txt`.

    Detailed Steps:
    a. Create the project directory.
    b. Create a virtual environment using the specified Python version.
    c. Install dependencies from the provided `requirements.txt` file (if available).
    d. Activate the virtual environment.

10. help                : Displays this help message.
    Usage:
    $ help
    Output: Displays the command reference with usage examples.

"""