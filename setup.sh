#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
SCRIPT_ENV="$SCRIPT_DIR/env";

echo "Creating virtual environment";
python3 -m venv "$SCRIPT_ENV";
source "$SCRIPT_ENV/bin/activate";
echo "Installing dependecies to local virtual environment";
pip3 install -r "$SCRIPT_DIRrequirements.txt";
deactivate;
