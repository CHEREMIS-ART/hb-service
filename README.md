# HB Service - Hotel Booking API

## Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- Poetry (для управления зависимостями)

### Установка и запуск

1. **Клонирование репозитория:**
```bash
git clone <repository-url>
cd hbservice
```

2. **Настройка окружения:**
```bash
# Копируем файл окружения
cp .env.example .env

# При необходимости редактируем .env
nano .env  # или используйте ваш любимый редактор
```

3. **Запуск приложения:**
```bash
# Запуск всех сервисов
make up

# Или напрямую через docker-compose
docker-compose up -d
```

4. **Проверка работы:**
```bash
# Проверить статус контейнеров
make ps

# Просмотр логов
make logs
```

Приложение будет доступно по адресу: http://localhost:8080

---

## API Documentation

### Базовый URL
```
http://localhost:8080/
```

## Hotels API

### 1. Создание номера отеля
**POST** `/hotels/create`

```bash
curl -X POST http://localhost:8080/hotels/create \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Люкс номер с видом на море",
    "price_per_night": "250.00"
  }'
```

**Ответ:**
```json
{
  "room_id": 1
}
```

### 2. Удаление номера отеля
**DELETE** `/hotels/delete/<room_id>`

```bash
curl -X DELETE http://localhost:8080/hotels/delete/1
```

### 3. Получение списка номеров
**GET** `/hotels/list`

```bash
curl -X GET "http://localhost:8080/hotels/list?sort_by=price_per_night&order=desc"
```

**Ответ:**
```json
[
  {
    "id": 1,
    "description": "Люкс номер с видом на море",
    "price_per_night": "250.00",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

## Bookings API

### 1. Создание бронирования
**POST** `/bookings/create`

```bash
curl -X POST http://localhost:8080/bookings/create \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "date_start": "2024-02-01",
    "date_end": "2024-02-05"
  }'
```

**Ответ:**
```json
{
  "booking_id": 1
}
```

### 2. Удаление бронирования
**DELETE** `/bookings/delete/<booking_id>`

```bash
curl -X DELETE http://localhost:8080/bookings/delete/1
```

### 3. Получение списка бронирований
**GET** `/bookings/list`

```bash
curl -X GET "http://localhost:8080/bookings/list?room_id=1"
```

**Ответ:**
```json
[
  {
    "id": 1,
    "room_id": 1,
    "date_start": "2024-02-01",
    "date_end": "2024-02-05"
  }
]
```
