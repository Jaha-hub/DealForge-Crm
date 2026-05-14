# LeadCustomField — Кастомное поле лида

**Таблица:** `lead_custom_fields`  
**Статус:** Domain + Infrastructure готовы; API — в разработке (MVP)

---

## Описание

Настраиваемое поле, которое `admin` или `director` добавляет к лидам. Позволяет адаптировать CRM под специфику бизнеса — добавлять любые атрибуты лидов без изменения кода.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `name` | VARCHAR(512) | NOT NULL | Название поля (уникальное среди активных) |
| `field_type` | VARCHAR(20) | NOT NULL, CHECK | Тип поля |
| `is_deleted` | BOOLEAN | NOT NULL, default=false | Soft delete флаг |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

**Уникальность имени:** `UNIQUE INDEX` на `(name)` с условием `WHERE is_deleted = FALSE` — два удалённых поля могут иметь одинаковое имя, два активных — нет.

---

## Типы полей (`field_type`)

| Значение | Описание | Пример использования |
|---|---|---|
| `text` | Свободный текст | «Название компании», «Откуда узнали» |
| `number` | Число (целое или дробное) | «Количество сотрудников», «Размер офиса» |
| `date` | Дата | «Дата встречи», «Дедлайн» |
| `time` | Время | «Время звонка» |
| `select_one` | Список — один вариант | «Категория клиента», «Приоритет» |
| `select_many` | Список — несколько флажков | «Интересующие услуги» |
| `boolean` | Да / Нет | «Согласен на рассылку», «Есть офис» |

---

## Бизнес-правила

- Создавать, переименовывать, удалять поля может только `admin` или `director`
- Для `select_one` и `select_many` обязателен хотя бы один элемент в [LeadCustomFieldEnum](lead-custom-field-enum.md)
- Для остальных типов список вариантов запрещён
- Удаление поля — **soft delete**; значения (`LeadCustomFieldValue`) у существующих лидов **сохраняются**
- Переименование поля не затрагивает существующие значения
- Восстановление удалённого поля (`is_deleted → false`) возможно, если нет активного поля с тем же именем

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| LeadCustomField → LeadCustomFieldEnum[] | One-to-Many | Варианты для select-полей |
| LeadCustomFieldValue.custom_field_id → LeadCustomField | Many-to-One | Значения у лидов |

---

## API эндпоинты (в разработке)

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| `GET` | `/api/v1/custom-fields/` | все | Список полей |
| `POST` | `/api/v1/custom-fields/` | admin, director | Создать поле |
| `PUT` | `/api/v1/custom-fields/{id}` | admin, director | Переименовать |
| `DELETE` | `/api/v1/custom-fields/{id}` | admin, director | Soft-delete |
| `POST` | `/api/v1/custom-fields/{id}/restore` | admin | Восстановить |
| `POST` | `/api/v1/custom-fields/{id}/enums` | admin, director | Добавить вариант enum |
| `DELETE` | `/api/v1/custom-fields/{id}/enums/{enum_id}` | admin, director | Удалить вариант enum |
