# LeadCustomFieldEnum — Вариант выбора кастомного поля

**Таблица:** `lead_custom_field_enums`  
**Статус:** Domain + Infrastructure готовы

---

## Описание

Один вариант значения для кастомных полей типа `select_one` и `select_many`. Пользователь видит эти варианты в выпадающем списке или в виде флажков при заполнении карточки лида.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `custom_field_id` | UUID | FK lead_custom_fields.id CASCADE | Поле, к которому принадлежит вариант |
| `value` | VARCHAR(255) | NOT NULL | Текст варианта |

---

## Бизнес-правила

- Принадлежит только полям типа `select_one` или `select_many`
- `value` уникален в пределах одного поля (два варианта не могут иметь одинаковый текст)
- Нельзя удалить вариант, если он используется хотя бы в одном `LeadCustomFieldValue`
- При удалении поля (`LeadCustomField`) — все варианты удаляются каскадно (ON DELETE CASCADE)
- Управлять вариантами может только `admin` или `director`

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| LeadCustomFieldEnum.custom_field_id → LeadCustomField | Many-to-One | Вариант принадлежит полю |
| LeadCustomFieldValue.enum_value → LeadCustomFieldEnum | Many-to-One (nullable) | Значение select_one указывает на вариант |

---

## API эндпоинты

Управляется через эндпоинты кастомных полей (см. [lead-custom-field.md](lead-custom-field.md)):

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/api/v1/custom-fields/{id}/enums` | Добавить вариант |
| `DELETE` | `/api/v1/custom-fields/{id}/enums/{enum_id}` | Удалить вариант |
