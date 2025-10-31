#!/bin/bash

# Функция которая выводит строку с префиксом "Hello, "
greet() {
    echo "Hello, $1"
}

# Функция которая возвращает сумму двух чисел
add_numbers() {
    local sum=$(($1 + $2))
    echo $sum
}

# Используем аргументы скрипта
greet "$1"
result=$(add_numbers $2 $3)
echo "$2 + $3 = $result"
