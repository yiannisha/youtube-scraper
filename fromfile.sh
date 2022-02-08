#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
SCRIPT_PATH="$SCRIPT_DIR/fileextract.py";
SCRIPT_ENV="$SCRIPT_DIR/env";

echo "$SCRIPT_ENV";

source "$SCRIPT_ENV/bin/activate";
python3 "$SCRIPT_PATH" "$1" "$2";
deactivate;
