#!/bin/bash

# Получаю абсолютную директорию скрипта
DIR="$(dirname "$(readlink -f "$0")")"

# Удаляю старую базу данных
rm "$DIR/app/db/dictionary.db"

# Восстанавливаю базу данных из бэкапа
sqlite3 "$DIR/app/db/dictionary.db" < "$DIR/app/db/dictionary.sql"
