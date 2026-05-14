# Notification — Уведомление

**Таблица:** `notifications`  
**Статус:** Планируется (MVP)

---

## Описание

In-app уведомление для пользователя о событиях в системе. Доставляется в реальном времени через WebSocket. Хранится в БД для отображения в ленте непрочитанных.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `user_id` | UUID | FK users.id, NOT NULL | Получатель уведомления |
| `title` | VARCHAR(255) | NOT NULL | Заголовок |
| `body` | TEXT | NOT NULL | Текст уведомления |
| `event_type` | VARCHAR(100) | NOT NULL, CHECK | Тип события |
| `payload` | JSONB | default={} | Дополнительные данные (например, lead_id) |
| `is_read` | BOOLEAN | NOT NULL, default=false | Прочитано ли |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |

---

## Типы событий (`event_type`)

| Значение | Кому отправляется | Триггер |
|---|---|---|
| `lead_assigned` | Назначенному консультанту | Лид назначен на пользователя |
| `stage_changed` | Назначенному | Лид переведён на другой этап |
| `lead_received` | Admin + Director | Новый лид поступил через webhook или форму |
| `lead_restored` | Sales Manager | Лид возвращён из `won`/`lost` в активный этап |

---

## Бизнес-правила

- Уведомления только читаются (is_read → true), **не удаляются** пользователем
- Доставка через **WebSocket** (`/ws/notifications`): при подключении клиент получает список непрочитанных, новые события приходят push-сообщением
- Счётчик непрочитанных отображается в хедере платформы
- `payload` содержит контекст для навигации (например, `{"lead_id": "uuid", "funnel_id": "uuid"}`)
- Уведомление создаётся **атомарно** вместе с действием (в рамках одной транзакции)

---

## WebSocket протокол

**Подключение:** `WS /ws/notifications` (требует JWT-токен в query или заголовке)

**При подключении** сервер отправляет:
```json
{
  "type": "init",
  "unread_count": 5,
  "notifications": [...]
}
```

**Новое уведомление** (push):
```json
{
  "type": "notification",
  "id": "uuid",
  "title": "Новый лид назначен",
  "body": "Лид «Иван Иванов» назначен на вас",
  "event_type": "lead_assigned",
  "payload": { "lead_id": "uuid" },
  "created_at": "2026-05-14T10:00:00Z"
}
```

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| Notification.user_id → User | Many-to-One | Получатель |

---

## API эндпоинты (в разработке)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/api/v1/notifications/` | Список уведомлений текущего пользователя |
| `PATCH` | `/api/v1/notifications/{id}/read` | Отметить прочитанным |
| `PATCH` | `/api/v1/notifications/read-all` | Отметить все прочитанными |
| `WS` | `/ws/notifications` | WebSocket-поток |
