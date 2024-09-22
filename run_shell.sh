#!/bin/sh

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate the virtual environment using the POSIX-compliant dot (.) instead of source
. venv/bin/activate

# Run your Python application
python3 -m app.main "$@"
