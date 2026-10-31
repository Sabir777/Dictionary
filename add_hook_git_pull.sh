#!/bin/bash

# создаю хук на восстановление БД из бэкапа при git pull
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash

./recovery_db.sh
EOF

chmod +x .git/hooks/post-merge
