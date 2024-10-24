### Welcome message
WELCOME_MESSAGE = """        
████████╗███████╗██████╗ ███╗   ███╗██╗██████╗ ██╗   ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔══██╗╚██╗ ██╔╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██████╔╝ ╚████╔╝ 
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██╔═══╝   ╚██╔╝  
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║        ██║   
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝        ╚═╝   
                                                        
Welcome to TermiPy!

Type 'help' for a list of available commands and their usage.

Author: Pratik Kumar
Version: 0.2.7
Date: 2024-10-24
Contact: pr2tik1@gmail.com
"""

HELP_MESSAGE = """
Available commands:

File Operations:
  tree       - Display directory structure in a tree-like format
  create     - Create a new file or directory
  search     - Search for files and directories
  delete     - Delete a file or directory
  rename     - Rename a file or directory
  permissions- Check permissions of a file or directory

System Commands:
  echo       - Print a message to the console
  getwd      - Display the current working directory
  ls         - List directory contents
  setwd      - Change the current working directory
  typeof     - Display the type of a file or directory
  clear      - Clear the console screen (aliases: cls, clr)
  diskusage  - Display disk usage information

Environment Setup:
  setpyenv   - Set up a Python virtual environment
  setrenv    - Set up an R environment
  createdevcontainer - Create a devcontainer (Remote Containers Extension for VSCode)

Utility Commands:
  help       - Display this help message
  about      - Display information about TermiPy
  commands   - List all available commands

Resource Monitoring:
  resource   - Display system resource usage information (aliases: resources, stats)

Other:
  exit       - Exit the TermiPy shell

Type '<command> -h' for more information on a specific command.
"""
