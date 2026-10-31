#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"

# создаю виртуальное окружение для запуска скриптов python
python3 -m venv "$DIR/sql_venv"

# уcтанавливаю зависимости в виртуальное окружение
source "$DIR/sql_venv/bin/activate"
pip install -r "$DIR/requirements.txt"

# восстанавливаю бэкап базы данных
sqlite3 "$DIR/app/db/dictionary.db" < "$DIR/app/db/dictionary.sql"

# создаю хук на восстановление БД из бэкапа при git pull
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash

./recovery_db.sh
EOF

chmod +x .git/hooks/post-merge
