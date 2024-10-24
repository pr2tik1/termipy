"""
Environment-related commands for TermiPy.

This module contains commands that deal with setting up development environments.
"""

import os
import subprocess
import sys
import json
from typing import List, Dict
from termipy.base_command import Command

class SetPyEnvCommand(Command):
    """Set up a Python virtual environment."""

    def execute(self, args: List[str]) -> bool:
        if self.handle_help_flag(args):
            return True

        if not args:
            print("Error: Please provide a name for the virtual environment.")
            return False

        env_name = args[0]
        try:
            subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
            print(f"Python virtual environment '{env_name}' created successfully.")
            print(f"To activate, run: source {env_name}/bin/activate (Unix) or {env_name}\\Scripts\\activate (Windows)")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to create Python virtual environment '{env_name}'.")
        return True

    def print_help(self):
        super().print_help()
        print("\nOptions:")
        print("  <env_name>  The name of the virtual environment to create.")
        print("\nExample:")
        print("  setpyenv myenv")

class SetREnvCommand(Command):
    """Set up an R environment."""

    def execute(self, args: List[str]) -> bool:
        if self.handle_help_flag(args):
            return True

        if not args:
            print("Error: Please provide a name for the R environment.")
            return False

        env_name = args[0]
        try:
            r_script = f"""
            if (!require(renv)) install.packages("renv")
            renv::init(project = "{env_name}")
            """
            subprocess.run(["Rscript", "-e", r_script], check=True)
            print(f"R environment '{env_name}' created successfully.")
            print(f"To use, set your working directory to '{env_name}' and run library(renv)")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to create R environment '{env_name}'.")
        except FileNotFoundError:
            print("Error: R is not installed or not in the system PATH.")
        return True

    def print_help(self):
        super().print_help()
        print("\nOptions:")
        print("  <env_name>  The name of the R environment to create.")
        print("\nExample:")
        print("  setrenv myenv")
        
        
class CreateDevContainerCommand(Command):
    """Create a DevContainer configuration."""

    def execute(self, args: List[str]) -> bool:
        if self.handle_help_flag(args):
            return True

        print("Welcome to TermiPy's DevContainer Creator!")
        
        use_custom = self._prompt("Do you have a custom devcontainer.json file? (y/n)").lower() == 'y'
        
        if use_custom:
            custom_path = self._prompt("Enter the path to your custom devcontainer.json file")
            if not os.path.exists(custom_path):
                print(f"Error: File not found at {custom_path}")
                return False
            
            try:
                with open(custom_path, 'r') as f:
                    devcontainer_config = json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in the provided file.")
                return False
        else:
            container_name = self._prompt("Container name")
            image_url = self._prompt("Image URL or Custom Image location")
            
            features = self._get_features()
            extensions = self._get_extensions()
            additional_settings = self._get_additional_settings()
            
            devcontainer_config = {
                "name": container_name,
                "image": image_url,
                "features": features,
                "extensions": extensions,
                "settings": additional_settings
            }
        
        project_path = os.getcwd()
        os.makedirs(os.path.join(project_path, '.devcontainer'), exist_ok=True)

        config_path = os.path.join(project_path, '.devcontainer', 'devcontainer.json')
        with open(config_path, 'w') as f:
            json.dump(devcontainer_config, f, indent=4)

        print(f"DevContainer configuration created at {config_path}")
        return True

    def print_help(self):
        super().print_help()
        print("\nThis command creates a DevContainer configuration interactively or from a custom file.")
        print("\nOptions:")
        print("  No command-line options. The command will prompt for necessary information.")
        print("\nExample:")
        print("  createdevcontainer")

    def _prompt(self, message: str) -> str:
        return input(f"{message}: ").strip()

    def _get_features(self) -> Dict[str, str]:
        features = {}
        if self._prompt("Include Git feature? (y/n)").lower() == 'y':
            features["git"] = "latest"
        if self._prompt("Include Python feature? (y/n)").lower() == 'y':
            features["python"] = "latest"
        return features

    def _get_extensions(self) -> List[str]:
        extensions_input = self._prompt("Add any VS Code extensions (comma-separated)")
        return [ext.strip() for ext in extensions_input.split(',') if ext.strip()]

    def _get_additional_settings(self) -> Dict[str, str]:
        settings = {}
        while True:
            key = self._prompt("Enter additional setting key (or press Enter to finish)")
            if not key:
                break
            value = self._prompt(f"Enter value for {key}")
            settings[key] = value
        return settings