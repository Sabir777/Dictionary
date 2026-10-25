#!/bin/bash

# Получаю абсолютную директорию скрипта
DIR="$(dirname "$(readlink -f "$0")")"

sqlite3 "$DIR/app/db/dictionary.db" < "$DIR/app/db/dictionary.sql"
