# Lead — Лид

**Таблица:** `leads`  
**Статус:** Domain готов; Infrastructure + API — в разработке (MVP)

---

## Описание

Центральная сущность платформы. Лид — потенциальный клиент, поступивший из какого-либо источника и проходящий путь по воронке продаж до закрытия сделки.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL | Имя или название лида |
| `phone` | VARCHAR(20) | nullable | Номер телефона |
| `email` | VARCHAR(320) | nullable | Email-адрес |
| `comment` | TEXT | nullable | Заметки / комментарий менеджера |
| `tags` | TEXT[] | default=[] | Теги для сегментации |
| `source_id` | UUID | FK sources.id, NOT NULL | Источник, откуда поступил лид |
| `funnel_id` | UUID | FK funnels.id, NOT NULL | Воронка, в которой находится лид |
| `stage_id` | UUID | FK funnel_stages.id, NOT NULL | Текущий этап воронки |
| `assign_to` | UUID | FK users.id, nullable | Ответственный менеджер / консультант |
| `is_deleted` | BOOLEAN | NOT NULL, default=false | Soft delete флаг |
| `closed_at` | TIMESTAMP WITH TZ | nullable | Дата закрытия (won/lost) |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

> **Контакт:** Хотя бы одно из полей `phone`, `email` должно быть заполнено (валидация на уровне домена через `Contact` value object).

---

## Жизненный цикл лида

```
[Создан] → [initial этап] → [intermediate этапы] → [won] или [lost]
                                                         │
                                                   closed_at = now()
```

- Лид **всегда** принадлежит ровно одной воронке
- Перемещение между этапами происходит вручную или автоматически (webhook)
- При переводе на этап `won` или `lost` — система записывает `closed_at`
- Возврат из `won`/`lost` в промежуточный этап обнуляет `closed_at`

---

## Бизнес-правила

- `stage_id` обязан принадлежать воронке `funnel_id` данного лида
- `name` должен быть от 2 до 255 символов
- `phone` или `email` — хотя бы одно заполнено
- `consultant` видит **только** лиды, где `assign_to = текущий пользователь`
- `sales_manager` видит лиды своей команды
- `director` и `admin` видят все лиды
- Удаление — soft delete; только `director` и `admin`
- Восстановление удалённого лида — только `admin`

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| Lead.source_id → Source | Many-to-One | Источник поступления |
| Lead.funnel_id → Funnel | Many-to-One | Воронка лида |
| Lead.stage_id → FunnelStage | Many-to-One | Текущий этап |
| Lead.assign_to → User | Many-to-One (nullable) | Ответственный |
| Lead → LeadCustomFieldValue[] | One-to-Many | Значения кастомных полей |
| Lead → LeadHistory[] | One-to-Many | История изменений |

---

## Операции

| Операция | Кто может |
|---|---|
| Создать лид вручную | sales_manager, director, admin; consultant — в любой воронке |
| Просмотреть лид | Согласно правилам видимости роли |
| Редактировать поля | Назначенный, sales_manager, director, admin |
| Перевести на другой этап | Назначенный, sales_manager, director, admin |
| Назначить менеджера | sales_manager, director, admin |
| Удалить (soft) | director, admin |
| Восстановить | admin |

---

## API эндпоинты (в разработке)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/api/v1/leads/` | Список лидов (фильтры: funnel, stage, source, assign_to, tags, period) |
| `POST` | `/api/v1/leads/` | Создать лид |
| `GET` | `/api/v1/leads/{id}` | Детали лида |
| `PUT` | `/api/v1/leads/{id}` | Обновить лид |
| `DELETE` | `/api/v1/leads/{id}` | Soft-delete |
| `PATCH` | `/api/v1/leads/{id}/stage` | Перевести на другой этап |
| `PATCH` | `/api/v1/leads/{id}/assign` | Назначить менеджера |
| `GET` | `/api/v1/leads/{id}/history` | История изменений |
