#!/bin/bash

# Exit if any command fails
set -e

echo "Creating Flake8 configuration..."
cat <<EOF > setup.cfg
[flake8]
max-line-length = 88
exclude = .git,__pycache__,build,dist
EOF

echo "Creating MyPy configuration..."
cat <<EOF > mypy.ini
[mypy]
ignore_missing_imports = True
disallow_untyped_defs = True
warn_unused_ignores = True
EOF

echo "Creating Pytest configuration..."
cat <<EOF > pytest.ini
[pytest]
addopts = --cov=src --cov-report=term-missing
testpaths = tests
EOF

echo "Setup complete! Config files created."