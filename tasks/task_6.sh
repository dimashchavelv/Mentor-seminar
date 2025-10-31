#!/bin/bash

# 1. Чтение данных из файла input.txt
echo "Содержимое input.txt:"
cat input.txt

# 2. Подсчет строк и запись в output.txt
wc -l input.txt > output.txt
echo "Результат подсчета строк записан в output.txt"

# 3. Перенаправление ошибок в error.log
ls несуществующий_файл 2> error.log
echo "Ошибки записаны в error.log"

# Показать результаты
echo -e "\nСодержимое output.txt:"
cat output.txt
echo -e "\nСодержимое error.log:"
cat error.log
