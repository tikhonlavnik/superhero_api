# Superhero API

Данный проект реализует REST API для работы с информацией о супергероях, получая данные из внешнего источника [superheroapi.com](https://superheroapi.com/) и сохраняя их в базу данных.

---

## Технические требования

- **Бэкенд**: FastAPI (Python)
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy (асинхронный режим)
- **Контейнеризация**: Docker + Docker Compose
- **Тестирование**: pytest
- **Внешнее API**: [https://superheroapi.com/](https://superheroapi.com/)

---

## Функционал

### 1. `POST /hero/` — Добавить героя в базу
- **Параметр**: `name` (обязательный)
- Запрашивает данные о герое по имени через `https://superheroapi.com/api/{token}/search/{name}`
- Если герой найден — сохраняет в БД
- Если герой не найден — возвращает ошибку `404 Not Found`

### 2. `GET /hero/` — Получить героев с фильтрами
- **Параметры (необязательные)**:
  - `name` — точное совпадение имени
  - `intelligence`, `strength`, `speed`, `power` — поддерживают фильтрацию
- Если герои не найдены — возвращает `404 Not Found`

---

## Установка и запуск

### Предварительные требования
- Установленный `Docker`


### Запуск проекта

1. Убедитесь, что Docker и Docker Compose установлены
2. Выполните команду:

```bash
docker-compose up -d --build
```

3. API будет доступно по адресу http://localhost:5000/

4. Для остановки проекта выполните:

```bash
docker-compose down
```

---

## Запуск тестов

```bash
docker-compose exec app pytest -v
```
