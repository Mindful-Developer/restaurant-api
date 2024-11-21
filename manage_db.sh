#!/bin/bash

# Check if the script is called with the correct number of arguments
if [ "$1" != "setup" ] && [ "$1" != "teardown" ]; then
    echo "Usage: ./manage_db.sh [setup|teardown]"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "Error: AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is required but not installed."
    exit 1
fi

# Check if running in virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment is activated"
else
    echo "Virtual environment is not activated. Please activate it first."
    exit 1
fi

# Run the appropriate script
if [ "$1" == "setup" ]; then
    python scripts/basic_setup.py
elif [ "$1" == "teardown" ]; then
    python scripts/basic_teardown.py
else
    echo "Error: Invalid argument."
fi