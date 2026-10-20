#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"
exec "$DIR/sql_venv/bin/python" "$DIR/app/main.py"
