#!/bin/bash

# Создаем временный alias
alias ll='ls -la'

# Демонстрация alias
echo "Демонстрация alias ll:"
ll

# Инструкция для постоянного добавления
echo "Для постоянного добавления выполните:"
echo "echo \"alias ll='ls -la'\" >> ~/.bashrc"
echo "source ~/.bashrc"

echo "Автодополнение для cd работает при нажатии Tab"
