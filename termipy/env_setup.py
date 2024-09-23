import os
import sys
import subprocess
import readline
import venv

def create_virtual_environment(python_version, project_name, req_file):
    """Create a virtual environment and install requirements."""
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    sys.stdout.write(f"Created project directory: {project_name}\n")

    python_executable = f"python{python_version}"
    if subprocess.run([python_executable, "--version"], capture_output=True).returncode != 0:
        sys.stdout.write(f"Error: Python {python_version} is not installed or not found.\n")
        return
    
    venv_dir = os.path.join(project_name, 'venv')
    sys.stdout.write(f"Creating virtual environment with Python {python_version}...\n")
    venv.create(venv_dir, with_pip=True)
    activate_script = os.path.join(venv_dir, 'bin', 'activate') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'activate')
    sys.stdout.write(f"Activating virtual environment...\n")
    
    if req_file and os.path.exists(req_file):
        sys.stdout.write(f"Installing requirements from {req_file}...\n")
        subprocess.run([os.path.join(venv_dir, 'bin', 'pip'), 'install', '-r', req_file])
    else:
        sys.stdout.write("No valid requirements.txt found.\n")