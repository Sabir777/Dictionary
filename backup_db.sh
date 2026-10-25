#!/bin/bash

# Получаю абсолютную директорию скрипта
DIR="$(dirname "$(readlink -f "$0")")"

# выполняю бэкап базы данных
sqlite3 "$DIR/app/db/dictionary.db" .dump > "$DIR/app/db/dictionary.sql"
