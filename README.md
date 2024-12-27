# Инструкция по запуску
1. Создать файл .env по примеру .env.example
2. docker compose up --build -d

# Структура базы данных
- id - int, primary key
- user_id - int, id пользователя в Telegram
- request - str, сообщение от пользователя
- response - str, ответ на сообщение пользователя