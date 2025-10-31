#!/bin/bash

# Запрашиваем ввод числа
read -p "Введите число: " number

# Проверяем положительное, отрицательное или ноль
echo "Проверка числа:"
if [ $number -gt 0 ]; then
    echo "Число положительное"
elif [ $number -lt 0 ]; then
    echo "Число отрицательное"
else
    echo "Число равно нулю"
fi

# Если число положительное, считаем от 1 до этого числа
if [ $number -gt 0 ]; then
    echo "Счет от 1 до $number:"
    counter=1
    while [ $counter -le $number ]; do
        echo $counter
        counter=$((counter + 1))
    done
fi
