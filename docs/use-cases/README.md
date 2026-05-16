# Use Cases — DealForge CRM

Полный список use case'ов платформы, сгруппированных по сущностям.

---

## Навигация

| Файл | Описание | Use Cases |
|---|---|---|
| [auth.md](auth.md) | Аутентификация и авторизация | UC-AUTH-01..05 |
| [user.md](user.md) | Управление пользователями | UC-USER-01..03 |
| [funnel.md](funnel.md) | Воронки продаж | UC-FUNNEL-01..05 |
| [funnel-stage.md](funnel-stage.md) | Этапы воронки | UC-STAGE-01..04 |
| [source.md](source.md) | Источники лидов | UC-SOURCE-01..10 |
| [lead.md](lead.md) | Лиды | UC-LEAD-01..09 |
| [lead-custom-field.md](lead-custom-field.md) | Кастомные поля | UC-FIELD-01..05 |
| [lead-custom-field-enum.md](lead-custom-field-enum.md) | Варианты выбора (enum) | UC-ENUM-01..02 |
| [lead-custom-field-value.md](lead-custom-field-value.md) | Значения кастомных полей | UC-FVAL-01..02 |
| [notification.md](notification.md) | Уведомления | UC-NOTIF-01..04 |
| [analytics.md](analytics.md) | Аналитика | UC-ANALYTICS-01..05 |

---

## Соглашения

### Структура каждого use case

```
ID        — уникальный идентификатор (UC-<ДОМЕН>-<NN>)
Название  — человекочитаемое название
Актор     — кто инициирует (роль или система)
Предусловия — что должно быть истинно до начала
Порядок действий — пошаговый основной сценарий
Что решает — бизнес-логика и ценность
Альтернативы — ошибки и нестандартные пути
Постусловия — что изменилось в системе после успеха
```

### Роли акторов

| Тег | Роль |
|---|---|
| `admin` | Администратор системы |
| `director` | Руководитель |
| `sales_manager` | Менеджер по продажам |
| `consultant` | Консультант / агент |
| `system` | Автоматическое системное действие |
| `anonymous` | Неавторизованный пользователь |
