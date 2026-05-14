# Сущности DealForge CRM — Обзор

## Список сущностей

| Сущность | Файл | Статус |
|---|---|---|
| User | [user.md](user.md) | Реализовано |
| Funnel | [funnel.md](funnel.md) | Реализовано |
| FunnelStage | [funnel-stage.md](funnel-stage.md) | Реализовано |
| Source | [source.md](source.md) | Реализовано |
| Lead | [lead.md](lead.md) | Domain готов, Infrastructure + API — в разработке |
| LeadCustomField | [lead-custom-field.md](lead-custom-field.md) | Domain + Infrastructure готовы, API — в разработке |
| LeadCustomFieldEnum | [lead-custom-field-enum.md](lead-custom-field-enum.md) | Domain + Infrastructure готовы |
| LeadCustomFieldValue | [lead-custom-field-value.md](lead-custom-field-value.md) | Domain готов, Infrastructure — в разработке |
| Notification | [notification.md](notification.md) | Планируется (MVP) |
| LeadHistory | [lead-history.md](lead-history.md) | Планируется (MVP) |

---

## Карта связей

```
User ──────────────────────────────────────────────────┐
 │                                                      │
 │ assign_to                                   created_by (история)
 ▼                                                      │
Lead ──── source_id ──► Source                          │
 │                                                      │
 │ funnel_id ──► Funnel ──► FunnelStage ◄── stage_id ──┘
 │                              ▲
 │ stage_id ────────────────────┘
 │
 ├── LeadCustomFieldValue[] ──► LeadCustomField
 │                                    │
 │                                    └──► LeadCustomFieldEnum[]
 │
 ├── LeadHistory[]
 │
 └── Notification[] ──► User
```

### Описание связей

| От | К | Тип | Поле |
|---|---|---|---|
| Lead | Funnel | Many-to-One | `Lead.funnel_id` |
| Lead | FunnelStage | Many-to-One | `Lead.stage_id` |
| Lead | Source | Many-to-One | `Lead.source_id` |
| Lead | User | Many-to-One (nullable) | `Lead.assign_to` |
| FunnelStage | Funnel | Many-to-One | `FunnelStage.funnel_id` |
| LeadCustomFieldValue | Lead | Many-to-One | `LeadCustomFieldValue.lead_id` |
| LeadCustomFieldValue | LeadCustomField | Many-to-One | `LeadCustomFieldValue.custom_field_id` |
| LeadCustomFieldEnum | LeadCustomField | Many-to-One | `LeadCustomFieldEnum.custom_field_id` |
| LeadHistory | Lead | Many-to-One | `LeadHistory.lead_id` |
| LeadHistory | User | Many-to-One (nullable) | `LeadHistory.user_id` |
| Notification | User | Many-to-One | `Notification.user_id` |

---

## Бизнес-правила уровня платформы

- Лид принадлежит ровно **одной** воронке одновременно
- `stage_id` лида всегда принадлежит воронке `funnel_id` того же лида
- `consultant` видит только лидов, **назначенных** на него; может создавать лиды в **любой** воронке (ограничение только логикой, не FK)
- Удаление сущностей — **soft delete** (флаг `is_deleted`); физического удаления нет
- Все временные метки хранятся в `UTC`, отображаются в `UTC+5` (Ташкент)

---

## Соглашения по именованию

| Категория | Соглашение | Пример |
|---|---|---|
| Таблицы БД | snake_case, множественное число | `lead_custom_fields` |
| Первичный ключ | `id UUID` | `id` |
| Внешний ключ | `<entity>_id` | `funnel_id`, `source_id` |
| Soft delete | `is_deleted BOOLEAN` | `is_deleted` |
| Временные метки | `created_at`, `updated_at` | — |
| Enum-колонки | `VARCHAR` + CHECK constraint | `field_type`, `kind`, `role` |
| JSON-конфиги | `JSONB` | `config` в Source |
