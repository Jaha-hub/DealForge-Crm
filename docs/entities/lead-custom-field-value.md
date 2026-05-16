# LeadCustomFieldValue — Значение кастомного поля лида

**Таблица:** `lead_custom_field_values`  
**Статус:** Domain готов; Infrastructure — в разработке (MVP)

---

## Описание

Хранит конкретное значение кастомного поля для конкретного лида. Каждая запись — пара «лид + поле = значение». Для `select_many` один лид может иметь несколько записей с одним `custom_field_id`.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `lead_id` | UUID | FK leads.id ON DELETE CASCADE | Лид |
| `custom_field_id` | UUID | FK lead_custom_fields.id | Поле |
| `value_text` | TEXT | nullable | Значение типа `text` |
| `value_number` | NUMERIC | nullable | Значение типа `number` |
| `value_date` | DATE | nullable | Значение типа `date` |
| `value_time` | TIME | nullable | Значение типа `time` |
| `value_boolean` | BOOLEAN | nullable | Значение типа `boolean` |
| `enum_value` | UUID | FK lead_custom_field_enums.id, nullable | Выбранный вариант для `select_one` |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

---

## Как хранится значение по типу поля

| Тип поля | Используемая колонка | Примечание |
|---|---|---|
| `text` | `value_text` | Свободный текст |
| `number` | `value_number` | Число |
| `date` | `value_date` | Только дата, без времени |
| `time` | `value_time` | Только время |
| `boolean` | `value_boolean` | true / false |
| `select_one` | `enum_value` | UUID варианта из `lead_custom_field_enums` |
| `select_many` | `enum_value` | Несколько строк с одним `custom_field_id`, по строке на вариант |

---

## Бизнес-правила

- В одной строке заполнена ровно **одна** колонка значения (остальные NULL) — валидация через `FieldValue` value object
- При удалении лида (`leads.id`) — все значения удаляются каскадно
- При soft delete поля (`LeadCustomField.is_deleted = true`) — значения **сохраняются** (поле скрыто, данные не теряются)
- Нельзя сохранить `enum_value`, не принадлежащий указанному `custom_field_id`
- Для `select_one` — на один лид максимум **одна** запись с данным `custom_field_id`
- Для `select_many` — на один лид может быть **несколько** записей с одним `custom_field_id`

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| LeadCustomFieldValue.lead_id → Lead | Many-to-One | Принадлежит лиду |
| LeadCustomFieldValue.custom_field_id → LeadCustomField | Many-to-One | Ссылка на определение поля |
| LeadCustomFieldValue.enum_value → LeadCustomFieldEnum | Many-to-One (nullable) | Выбранный вариант |
