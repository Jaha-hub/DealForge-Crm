# Funnel — Воронка продаж

**Таблица:** `funnels`  
**Статус:** Реализовано (Domain + Infrastructure + API)

---

## Описание

Воронка продаж — это набор упорядоченных этапов, через которые проходит лид от первого контакта до закрытия сделки. Один аккаунт может иметь несколько воронок под разные процессы продаж.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL | Название воронки |
| `is_deleted` | BOOLEAN | NOT NULL, default=false | Soft delete флаг |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

---

## Бизнес-правила

- Лид принадлежит ровно **одной** воронке одновременно
- Удаление воронки — **soft delete** (`is_deleted = true`); данные сохраняются
- При soft delete лиды, находящиеся в воронке, остаются привязанными к ней
- Только `admin` и `director` могут создавать, изменять и удалять воронки
- В воронке должен быть хотя бы один этап типа `initial`

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| Funnel → FunnelStage[] | One-to-Many | Воронка содержит упорядоченные этапы |
| Lead.funnel_id → Funnel | Many-to-One | Лид принадлежит воронке |
| Source.config.funnel_id → Funnel | (логическая) | Webhook/Form источник привязан к воронке |

---

## API эндпоинты

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| `POST` | `/api/v1/funnels/` | admin, director | Создать воронку |
| `GET` | `/api/v1/funnels/{id}` | все | Получить воронку |
| `PUT` | `/api/v1/funnels/funnel_update/{id}` | admin, director | Переименовать воронку |
| `DELETE` | `/api/v1/funnels/{id}` | admin | Soft-delete воронки |
| `GET` | `/api/v1/funnels/{id}/stages` | все | Список этапов воронки |
