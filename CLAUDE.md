# CLAUDE.md — DealForge CRM

Этот файл описывает проект, принятые решения и текущее состояние разработки.
Читай его в начале каждой сессии.

---

## Что это за проект

**DealForge CRM** — SaaS CRM-платформа для малого бизнеса на рынке Узбекистана.

Основные возможности:
- Воронки продаж с Kanban-доской
- Лиды из разных источников (ручной ввод, webhook, публичная форма)
- Кастомные поля для лидов (7 типов)
- Аналитика: конверсия воронки, эффективность менеджеров, источники, динамика
- In-app уведомления через WebSocket

**Документация проекта:**
- PRD: `docs/PRD.md`
- Сущности: `docs/entities/README.md` + отдельный файл на каждую сущность

---

## Технологический стек

| Слой | Технология |
|---|---|
| Backend | FastAPI, Python 3.13, Clean Architecture (DDD) |
| ORM | SQLAlchemy async + asyncpg |
| БД | PostgreSQL (JSONB для конфигов источников) |
| Auth | JWT (access 2h / refresh 7d), Argon2 |
| Миграции | Alembic |
| Frontend | Next.js + TypeScript (Web + Mobile-responsive) |
| Деплой | SaaS (self-hosted VPS в Узбекистане) |
| Контейнеры | Docker / Docker Compose |

---

## Архитектура бэкенда

Чистая архитектура (Clean Architecture / DDD). Структура слоёв:

```
backend/src/backend/
├── domain/          # Сущности, value objects, политики, ошибки домена
├── application/     # Use cases, DTO, интерфейсы репозиториев
├── infrastructure/  # SQLAlchemy модели, репозитории, JWT, Argon2
└── presentation/    # FastAPI роутеры (CBV-стиль через fastapi_utils)
```

**Ключевые паттерны:**
- Unit of Work (`SqlalchemyUnitOfWork`) — управление транзакциями
- Repository Pattern — абстракция доступа к данным
- Value Objects — строгая типизация доменных концептов
- Mapper — конвертация entity ↔ SQLAlchemy model
- Dependency Injection через `Depends()` FastAPI

**Точка входа:** `backend/src/backend/main.py`  
**UoW:** `backend/src/backend/infrastructure/db/sqlalchemy/core/uow.py`  
**Зависимости:** `backend/src/backend/presentation/api/v1/core/dependencies.py`

---

## Роли пользователей

| Роль | Что может |
|---|---|
| `admin` | Всё: пользователи, воронки, источники, кастомные поля, аналитика |
| `director` | Просмотр всего, аналитика, управление воронками, назначение менеджеров |
| `sales_manager` | Своя команда: лиды, аналитика по команде |
| `consultant` | Только свои лиды (назначенные на него); может создавать лиды в любой воронке |

> Доступ consultant к воронкам — бизнес-правило, **не FK**. Отдельной таблицы `funnel_access` нет.

---

## Сущности и их статус

| Сущность | Domain | Infrastructure | API |
|---|---|---|---|
| User | ✅ | ✅ | ✅ |
| Funnel | ✅ | ✅ | ✅ |
| FunnelStage | ✅ | ✅ | ✅ |
| Source | ✅ | ✅ | ✅ |
| Lead | ✅ | ❌ нет | ❌ нет |
| LeadCustomField | ✅ | ✅ | ❌ нет |
| LeadCustomFieldEnum | ✅ | ✅ | через CustomField |
| LeadCustomFieldValue | ✅ | ❌ нет | ❌ нет |
| Notification | ❌ нет | ❌ нет | ❌ нет |
| LeadHistory | ❌ нет | ❌ нет | ❌ нет |

---

## Известные баги (исправлены в сессии)

Следующие баги были найдены и исправлены:

1. **`domain/lead/entity.py`** — `remove_enum()` использовал `==` вместо `!=` (фильтровал не те элементы)
2. **`domain/lead/entity.py`** — `set_custom_value()` не вызывал `_add_multi_value` / `_add_single_value`
3. **`infrastructure/.../lead/custom_field/repository.py`** — `list_all()` не возвращал результат
4. **`infrastructure/.../lead/custom_field/repository.py`** — `_fetch_enums()` использовал `list[result...]` вместо `list(result...)`
5. **`infrastructure/.../lead/custom_field/repository.py`** — `update()` неверная логика INSERT/UPDATE enum
6. **`infrastructure/.../lead/custom_field/repository.py`** — методы `remove()`, `get_all()`, `list_by_ids()` отсутствовали
7. **`application/lead/use_cases/custom_field/update_custom_field.py`** — `cmd.field` вместо `self.field`

---

## Что нужно реализовать (MVP)

### Бэкенд (в порядке приоритета)

1. **Lead Infrastructure** — SQLAlchemy model (`leads` таблица) + mapper + repository
2. **LeadCustomFieldValue Infrastructure** — `lead_custom_field_values` таблица
3. **LeadRepository** — интерфейс в `application/lead/repository.py`
4. **Lead Use Cases** — Create, Get, List, Update, Delete, ChangeStage, Assign
5. **Lead DTOs** — в `application/lead/dtos/lead/`
6. **Update UnitOfWork** — добавить `leads`, `custom_fields`, `source` в `SqlalchemyUnitOfWork`
7. **Lead API Router** — `presentation/api/v1/lead/`
8. **Custom Field API Router** — use cases готовы, нужны только роуты
9. **Webhook endpoint** — `POST /webhook/{source_id}` без auth
10. **Public Form endpoint** — `GET /forms/{source_id}` + `POST /forms/{source_id}/submit`
11. **Notification** — таблица + модель + WebSocket (`/ws/notifications`)
12. **LeadHistory** — таблица + логирование при изменениях лида
13. **Analytics** — `GET /api/v1/analytics/dashboard|funnel|sources|managers|dynamics`
14. **Alembic миграции** — для всех новых таблиц

### Фронтенд (Next.js)

- Kanban-доска воронки (drag-and-drop)
- Карточка лида (стандартные + кастомные поля)
- Управление воронками и этапами
- Управление источниками (webhook-ключ, embed публичной формы)
- Управление кастомными полями
- Дашборд аналитики
- Публичная форма (`/forms/{id}`)
- i18n: ru / uz / en

---

## Важные архитектурные решения

| Решение | Описание |
|---|---|
| Один лид = одна воронка | Лид не может быть в нескольких воронках одновременно |
| Soft delete везде | Физического удаления данных нет. Флаг `is_deleted` |
| Webhook — автосоздание лида | POST на `/webhook/{source_id}` → лид создаётся автоматически на первом `initial` этапе |
| Уведомления через WebSocket | Не polling. Endpoint: `/ws/notifications` |
| Мультитенантность — нет | Один инстанс = одна компания. Нет `company_id` |
| reCAPTCHA на форме — нет | Публичная форма без защиты от спама |
| LeadHistory в MVP | Журнал изменений — append-only таблица |
| Бюджет лида — нет | Не стандартное поле. Только через кастомные поля |

---

## Структура новых таблиц (к созданию)

### `leads`
```sql
id, name, phone, email, comment, tags TEXT[],
source_id FK, funnel_id FK, stage_id FK, assign_to FK nullable,
is_deleted, closed_at nullable, created_at, updated_at
```

### `lead_custom_field_values`
```sql
id, lead_id FK CASCADE, custom_field_id FK,
value_text, value_number, value_date, value_time, value_boolean,
enum_value FK nullable,
created_at, updated_at
```

### `lead_history`
```sql
id, lead_id FK, user_id FK nullable,
action VARCHAR(100), old_value JSONB, new_value JSONB,
created_at
```

### `notifications`
```sql
id, user_id FK, title, body,
event_type VARCHAR(100), payload JSONB,
is_read BOOLEAN default=false,
created_at
```

---

## Переменные окружения (backend/.env)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1
POSTGRES_NAME=Crm
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:1@localhost:5432/Crm

JWT_SECRET=secret
JWT_ACCESS_TOKEN_EXPIRES=2
JWT_REFRESH_TOKEN_EXPIRES=7
JWT_ALGORITHM=HS256
```

---

## Запуск проекта

```bash
cd backend
poetry install
alembic upgrade head
uvicorn src.backend.main:app --reload
```

---

## Roadmap

### MVP (1–2 месяца)
Всё из раздела «Что нужно реализовать» выше.

### Фаза 2 (после MVP)
- Telegram-уведомления
- Email-уведомления
- Экспорт/импорт лидов (Excel/CSV)
- Фильтрация по кастомным полям
- Mobile-приложение (React Native / Expo)
- Интеграции с мессенджерами (Telegram, WhatsApp)
- Автоматизации (триггеры по условиям)
