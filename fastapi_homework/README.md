# FastAPI Microservices: TODO + ShortURL (SQLite + Docker volumes)

Два микросервиса на FastAPI:
- TODO service (CRUD задач) — /docs на порту 8000
- ShortURL service (сокращение ссылок) — /docs на порту 8001

SQLite хранится в /app/data, подключаем как Docker volume.

## Запуск через Docker

### Создать тома
```bash
docker volume create todo_data
docker volume create shorturl_data

