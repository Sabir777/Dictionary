#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"
exec "$DIR/sql_venv/bin/python" "$DIR/app/main.py"

# выполняю бэкап базы данных
sqlite3 "$DIR/app/db/dictionary.db" .dump > "$DIR/app/db/dictionary.sql"
