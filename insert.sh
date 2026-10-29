#!/bin/bash

# Получаю абсолютную директорию скрипта
DIR="$(dirname "$(readlink -f "$0")")"

# Запуск приложения
"$DIR/sql_venv/bin/python" "$DIR/app/insert.py"

# выполняю бэкап базы данных
sqlite3 "$DIR/app/db/dictionary.db" .dump > "$DIR/app/db/dictionary.sql"
