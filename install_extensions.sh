#!/bin/bash

# Exit if any command fails
set -e

# Ensure Python and pip are installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Installing now..."
    python3 -m ensurepip --default-pip
fi

# Upgrade pip
pip3 install --upgrade pip

# Install required Python tools
pip3 install flake8 mypy pytest pytest-cov

# Verify installation
echo "Installed versions:"
flake8 --version
mypy --version
pytest --version

echo "Installation complete!"