# FunnelStage — Этап воронки

**Таблица:** `funnel_stages`  
**Статус:** Реализовано (Domain + Infrastructure + API)

---

## Описание

Этап внутри воронки продаж. Лид переходит между этапами по мере продвижения сделки. Каждый этап имеет тип (`kind`), определяющий его роль в процессе.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `funnel_id` | UUID | FK funnels.id CASCADE | Воронка, к которой принадлежит этап |
| `name` | VARCHAR(255) | NOT NULL | Название этапа |
| `win_probability` | INTEGER | NOT NULL, 0–100 | Вероятность закрытия сделки (%) |
| `hex` | VARCHAR(7) | NOT NULL | Цвет этапа в HEX-формате (`#RRGGBB`) |
| `order` | INTEGER | NOT NULL | Порядок отображения (меньше = левее) |
| `kind` | VARCHAR(100) | default='initial' | Тип этапа |
| `is_archived` | BOOLEAN | NOT NULL, default=false | Архивирован ли этап |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

---

## Типы этапов (`kind`)

| Значение | Описание | Поведение |
|---|---|---|
| `initial` | Первый этап (входящий) | Лиды из webhook/формы попадают сюда |
| `intermediate` | Промежуточный этап | Стандартная обработка |
| `won` | Сделка закрыта (успех) | При переходе: `Lead.closed_at = now()` |
| `lost` | Сделка закрыта (провал) | При переходе: `Lead.closed_at = now()` |

---

## Бизнес-правила

- В каждой воронке должен быть хотя бы **один** этап типа `initial`
- Этапы типа `won` и `lost` должны быть **хотя бы по одному** в воронке
- `order` уникален в пределах одной воронки
- Архивирование (`is_archived = true`) скрывает этап из Kanban-доски, но не удаляет
- Лиды на архивированном этапе остаются привязанными к нему
- При удалении воронки — все этапы удаляются каскадно (ON DELETE CASCADE)
- При переводе лида на `won`/`lost` система фиксирует `closed_at` у лида

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| FunnelStage.funnel_id → Funnel | Many-to-One | Этап принадлежит воронке |
| Lead.stage_id → FunnelStage | Many-to-One | Лид находится на этапе |

---

## API эндпоинты

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| `GET` | `/api/v1/funnels/{funnel_id}/stages` | все | Список этапов |
| `POST` | `/api/v1/funnels/{funnel_id}/stages/` | admin, director | Создать этап |
| `PUT` | `/api/v1/funnels/{funnel_id}/stages/{stage_id}` | admin, director | Обновить этап |
| `DELETE` | `/api/v1/funnels/{funnel_id}/stages/{stage_id}` | admin | Удалить этап |
