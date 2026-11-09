#!/bin/bash

echo "Введите текст на английском"
echo "Для завершения ввода нажите Ctrl-D"
echo "==============================="
while IFS= read -r line; do
    if [ -n "$line" ]; then
        echo "$line" | trans -e bing en:ru -brief -no-warn 2>/dev/null
    else
        echo
    fi
done >> text.txt

echo "============Перевод============"
cat text.txt
rm text.txt
