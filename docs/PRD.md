# PRD — DealForge CRM

**Версия:** 1.1  
**Дата:** 2026-05-14  
**Автор:** System Architect / PM  
**Статус:** В разработке

---

## 1. Обзор продукта

### 1.1 Что это

DealForge CRM — облачная (SaaS) CRM-платформа для малого бизнеса на локальном рынке Узбекистана. Система управляет лидами через настраиваемые воронки продаж, собирает заявки из разных источников (ручной ввод, webhook, публичная форма) и предоставляет аналитику по эффективности команды и источников.

### 1.2 Целевая аудитория

- Малый и средний бизнес Узбекистана (5–50 человек в отделе продаж)
- Отрасли: недвижимость, образование, e-commerce, услуги

### 1.3 Бизнес-цель MVP

Позволить команде продаж вести лидов по воронке, фиксировать результат по каждой сделке и видеть базовую аналитику — за 1–2 месяца разработки.

---

## 2. Стек и архитектура

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

## 3. Роли и права доступа

| Роль | Описание | Права |
|---|---|---|
| `admin` | Администратор системы | Полный доступ: пользователи, воронки, источники, кастомные поля, аналитика, настройки |
| `director` | Руководитель | Просмотр всех лидов и аналитики, назначение менеджеров, управление воронками |
| `sales_manager` | Менеджер по продажам | Управление своими лидами и лидами своей команды, просмотр аналитики по команде |
| `consultant` | Консультант/агент | Работа только со своими лидами, создание лидов вручную |

**Правила:**
- `consultant` видит только лидов, назначенных на него
- `consultant` может создавать лиды **только в воронках, к которым его допустил** `sales_manager` или `admin`
- `sales_manager` видит всех лидов своей команды
- `director` и `admin` видят всё

---

## 4. Основные сущности (текущее состояние бэкенда)

### 4.1 Уже реализовано

| Сущность | Статус |
|---|---|
| `User` | Domain + Infrastructure + API |
| `Funnel` + `FunnelStage` | Domain + Infrastructure + API |
| `Source` (manual/webhook/public_form) | Domain + Infrastructure + API |
| `LeadCustomField` + `LeadCustomFieldEnum` | Domain + Infrastructure (API отсутствует) |
| `Lead` | Domain (нет Infrastructure + API) |

### 4.2 Требуется разработать

- Lead: Infrastructure (SQLAlchemy model, repository) + API
- LeadCustomField: API (use cases готовы)
- LeadCustomFieldValue: связь значений кастомных полей с конкретным лидом
- Analytics: отдельный модуль запросов
- Notifications (in-app): модуль событий
- Public Form: публичный endpoint (без auth) для приёма заявок

---

## 5. Управление лидами

### 5.1 Поля лида по умолчанию

| Поле | Тип | Обязательное |
|---|---|---|
| `name` | string (до 255) | Да |
| `phone` | string (до 20) | Нет |
| `email` | string (до 320) | Нет |
| `comment` | text | Нет |
| `tags` | string[] | Нет |
| `source_id` | UUID → Source | Да |
| `funnel_id` | UUID → Funnel | Да |
| `stage_id` | UUID → FunnelStage | Да |
| `assign_to` | UUID → User | Нет |
| `custom_values` | LeadCustomFieldValue[] | Нет |
| `is_deleted` | bool | Системное |
| `created_at` | datetime | Системное |
| `updated_at` | datetime | Системное |

### 5.2 Кастомные поля

Пользователь (admin/director) создаёт дополнительные поля для лидов. Поддерживаемые типы:

| Тип (`field_type`) | Описание | Пример |
|---|---|---|
| `text` | Текстовое поле | «Название компании» |
| `number` | Числовое | «Количество сотрудников» |
| `date` | Дата | «Дата встречи» |
| `time` | Время | «Время звонка» |
| `select_one` | Список — один выбор | «Категория клиента» |
| `select_many` | Список — несколько флажков | «Интересующие услуги» |
| `boolean` | Флажок да/нет | «Согласен на рассылку» |

**Правила кастомных полей:**
- Имена полей уникальны (среди активных)
- Для `select_one` и `select_many` — список значений управляется отдельно (LeadCustomFieldEnum)
- Удаление поля — soft delete; значения существующих лидов сохраняются
- Переименование поля не затрагивает существующие значения

### 5.3 Воронка продаж

- Лид принадлежит **одной** воронке одновременно
- Лид проходит этапы последовательно (drag-and-drop в Kanban-виде или выбор вручную)
- У каждого этапа: название, цвет (hex), порядок, вероятность выигрыша (0–100%), тип (`initial` / `intermediate` / `won` / `lost`)
- При переводе лида на этап типа `won` или `lost` — фиксируется дата закрытия
- Один аккаунт может иметь несколько воронок (например, «Продажа курсов» и «Аренда офисов»)

### 5.4 Операции с лидами

| Операция | Доступно |
|---|---|
| Создать лид вручную | sales_manager, director, admin; consultant — только в доступных воронках |
| Перевести в следующий этап | Назначенный, sales_manager, director, admin |
| Назначить менеджера | sales_manager, director, admin |
| Редактировать поля | Назначенный, sales_manager, director, admin |
| Удалить лид (soft) | director, admin |
| Восстановить лид | admin |
| Добавить/изменить кастомные значения | Назначенный, sales_manager, director, admin |

---

## 6. Источники лидов

### 6.1 Типы источников

#### Manual
- Лид создаётся менеджером вручную через интерфейс
- При создании пользователь выбирает воронку и первый этап

#### Webhook
- Внешняя система (сайт, бот, форма) делает `POST /api/v1/webhook/{source_id}`
- Запрос должен содержать заголовок `X-Webhook-Secret: <token>`
- Backend верифицирует токен через `source.verify_webhook_token()`
- При успехе — автоматически создаётся лид в привязанной воронке на первом (`initial`) этапе
- **Маппинг полей:** в конфиге источника (`config`) хранится маппинг: поле входящего JSON → поле лида
- Пример входящего payload:
  ```json
  {
    "name": "Иван Иванов",
    "phone": "+998901234567",
    "email": "ivan@example.com"
  }
  ```
- Невалидные запросы (неверный токен, неверный payload) возвращают `400`/`401` и логируются

#### Public Form
- Система генерирует публичную форму с уникальным URL
- URL доступен без авторизации
- Пользователь заполняет форму на сайте/по ссылке → лид создаётся автоматически
- Admin настраивает: какие поля показывать на форме (из стандартных + кастомных)

### 6.2 Управление источниками

- Создание, редактирование, деактивация/активация, удаление (soft)
- Для webhook: регенерация секрета (`regenerate-webhook-secret`)
- Фильтрация по типу и статусу

---

## 7. Аналитика

### 7.1 Дашборд (главная страница)

**Виджеты:**
| Виджет | Описание |
|---|---|
| Всего лидов | Счётчик за выбранный период |
| Конверсия | % лидов, дошедших до `won` |
| Открытые лиды | По воронкам |
| Лиды по источникам | Pie chart: Manual / Webhook / Public Form |

### 7.2 Воронка продаж (Funnel Analytics)

- Визуализация воронки: количество лидов на каждом этапе
- Конверсия между этапами (этап N → этап N+1)
- Среднее время нахождения лида на каждом этапе
- Фильтры: воронка, период, ответственный менеджер

### 7.3 Источники лидов

- Таблица и график: количество лидов по каждому источнику
- Конверсия в `won` по источнику
- Динамика по времени (день / неделя / месяц)

### 7.4 Эффективность менеджеров

- Таблица: менеджер → количество лидов → количество `won` → конверсия
- Среднее время закрытия сделки
- Фильтр по периоду

### 7.5 Динамика за период

- График новых лидов (ось X: дата, ось Y: количество)
- График закрытых сделок (`won` / `lost`)
- Выбор периода: вчера / неделя / месяц / квартал / произвольный диапазон

---

## 8. Уведомления (In-App)

| Событие | Кому |
|---|---|
| Новый лид назначен на тебя | Назначенному консультанту |
| Лид переведён на новый этап | Назначенному |
| Новый лид поступил через webhook/форму | Admin + Director |
| Лид возвращён (из `won`/`lost`) | Sales Manager |

**Реализация:**
- Хранение уведомлений в БД (таблица `notifications`)
- Доставка в реальном времени через **WebSocket** (`/ws/notifications`)
- При подключении клиент получает список непрочитанных; новые события приходят push-сообщением
- Счётчик непрочитанных в хедере
- Отметка "прочитано" по клику

---

## 9. Локализация

- Поддержка трёх языков: **Русский (ru)**, **Узбекский (uz)**, **Английский (en)**
- Язык выбирается в профиле пользователя
- Все строки интерфейса переведены через i18n (Next.js i18n routing)
- Дата/время отображаются в часовом поясе `UTC+5` (Ташкент)
- Валюта: узбекский сум (UZS)

---

## 10. Публичная форма (Technical Spec)

```
GET /forms/{source_id}          → HTML-страница формы (без auth)
POST /forms/{source_id}/submit  → Приём данных, создание лида
```

- Форма рендерится на основе конфигурации источника
- Успешная отправка → страница «Спасибо»
- Форма брендируется под название компании (лого, цвет)

---

## 11. API — новые эндпоинты (к разработке)

### Лиды (`/api/v1/leads`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/leads/` | Список лидов (фильтры: funnel, stage, source, assign_to, tags, period) |
| `POST` | `/leads/` | Создание лида |
| `GET` | `/leads/{lead_id}` | Детали лида |
| `PUT` | `/leads/{lead_id}` | Обновление лида |
| `DELETE` | `/leads/{lead_id}` | Soft-delete |
| `PATCH` | `/leads/{lead_id}/stage` | Перевод на другой этап |
| `PATCH` | `/leads/{lead_id}/assign` | Назначить менеджера |
| `GET` | `/leads/{lead_id}/history` | История изменений |

### Кастомные поля (`/api/v1/custom-fields`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/custom-fields/` | Список полей |
| `POST` | `/custom-fields/` | Создать поле |
| `PUT` | `/custom-fields/{id}` | Переименовать |
| `DELETE` | `/custom-fields/{id}` | Soft-delete |
| `POST` | `/custom-fields/{id}/enums` | Добавить значение enum |
| `DELETE` | `/custom-fields/{id}/enums/{enum_id}` | Удалить значение enum |

### Webhook endpoint

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/webhook/{source_id}` | Приём webhook, автосоздание лида |

### Аналитика (`/api/v1/analytics`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/analytics/dashboard` | Сводные показатели |
| `GET` | `/analytics/funnel/{funnel_id}` | Конверсия воронки |
| `GET` | `/analytics/sources` | Лиды по источникам |
| `GET` | `/analytics/managers` | Эффективность менеджеров |
| `GET` | `/analytics/dynamics` | Динамика за период |

### Уведомления (`/api/v1/notifications`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/notifications/` | Список уведомлений |
| `PATCH` | `/notifications/{id}/read` | Отметить прочитанным |
| `PATCH` | `/notifications/read-all` | Отметить все прочитанными |

---

## 12. Модель данных — новые таблицы

### `leads`
```sql
id            UUID PK
name          VARCHAR(255) NOT NULL
phone         VARCHAR(20)
email         VARCHAR(320)
comment       TEXT
tags          TEXT[]          -- массив тегов
source_id     UUID FK sources.id
funnel_id     UUID FK funnels.id
stage_id      UUID FK funnel_stages.id
assign_to     UUID FK users.id NULLABLE
is_deleted    BOOLEAN DEFAULT FALSE
closed_at     TIMESTAMP WITH TIME ZONE NULLABLE
created_at    TIMESTAMP WITH TIME ZONE
updated_at    TIMESTAMP WITH TIME ZONE
```

### `lead_custom_field_values`
```sql
id              UUID PK
lead_id         UUID FK leads.id ON DELETE CASCADE
custom_field_id UUID FK lead_custom_fields.id
value_text      TEXT NULLABLE
value_number    NUMERIC NULLABLE
value_date      DATE NULLABLE
value_time      TIME NULLABLE
value_boolean   BOOLEAN NULLABLE
enum_values     UUID[]  -- для select_many: массив LeadCustomFieldEnum.id
enum_value      UUID FK lead_custom_field_enums.id NULLABLE  -- для select_one
created_at      TIMESTAMP WITH TIME ZONE
updated_at      TIMESTAMP WITH TIME ZONE
```

### `lead_history`
```sql
id          UUID PK
lead_id     UUID FK leads.id
user_id     UUID FK users.id NULLABLE
action      VARCHAR(100)  -- stage_changed, field_updated, assigned, created, deleted
old_value   JSONB
new_value   JSONB
created_at  TIMESTAMP WITH TIME ZONE
```

### `notifications`
```sql
id          UUID PK
user_id     UUID FK users.id
title       VARCHAR(255)
body        TEXT
is_read     BOOLEAN DEFAULT FALSE
event_type  VARCHAR(100)
payload     JSONB
created_at  TIMESTAMP WITH TIME ZONE
```

---

## 13. Frontend — экраны

### Обязательные экраны MVP

| Экран | Описание |
|---|---|
| Авторизация | Login, смена пароля |
| Дашборд | Виджеты + сводка |
| Канбан-доска | Лиды по колонкам (этапы воронки), drag-and-drop |
| Список лидов | Таблица с фильтрами и сортировкой |
| Карточка лида | Все поля, история, кастомные значения, комментарий |
| Управление воронками | Список, создание, редактирование этапов |
| Источники | Список, создание, webhook-ключ, embed-код формы |
| Кастомные поля | Управление полями и enum-значениями |
| Аналитика | Вкладки: воронка / источники / менеджеры / динамика |
| Профиль | Смена языка, пароля |
| Пользователи | Admin: CRUD пользователей, назначение ролей |

### Публичная страница (без авторизации)
| Экран | Описание |
|---|---|
| Публичная форма | `/forms/{id}` — форма заявки |
| Страница успеха | После отправки формы |

---

## 14. Нефункциональные требования

| Требование | Значение |
|---|---|
| Время ответа API | < 300ms (p95) |
| Аутентификация | JWT, access 2h, refresh 7d |
| Безопасность webhook | HMAC/Bearer token per source |
| Часовой пояс | UTC+5 (Ташкент) |
| Языки | ru / uz / en |
| Мобильная адаптация | Responsive Web (Next.js), PWA |

---

## 15. Roadmap

### MVP (Фаза 1) — 1–2 месяца

**Бэкенд:**
- [ ] Lead: Infrastructure + API (CRUD, stage change, assign)
- [ ] LeadCustomFieldValue: Infrastructure + API
- [ ] Webhook endpoint (auto-create lead)
- [ ] Analytics endpoints (dashboard, funnel, sources, managers, dynamics)
- [ ] Notifications: модель + базовые события
- [ ] Lead history: логирование изменений

**Фронтенд:**
- [ ] Канбан-доска воронки
- [ ] Карточка лида (стандартные + кастомные поля)
- [ ] Управление воронками
- [ ] Управление источниками + webhook-ключ
- [ ] Управление кастомными полями
- [ ] Базовый дашборд аналитики
- [ ] Публичная форма (embed)
- [ ] i18n (ru/uz/en)

### Фаза 2 — после MVP

- Telegram-уведомления
- Email-уведомления
- Экспорт лидов в Excel/CSV
- Импорт лидов из CSV
- Фильтрация по кастомным полям
- Расширенный конструктор публичных форм (кастомный дизайн)
- Mobile-приложение (React Native / Expo)
- Интеграция с мессенджерами (Telegram, WhatsApp)
- SLA по стадиям (время на этапе)
- Автоматизации (правила: если лид в стадии X дольше Y дней → уведомить)

---

## 16. Решённые вопросы

| # | Вопрос | Решение |
|---|---|---|
| 1 | Мультитенантность? | Не нужна. Одна компания — один инстанс |
| 2 | Защита публичной формы от спама (reCAPTCHA)? | Не нужна |
| 3 | WebSocket или polling для уведомлений? | WebSocket |
| 4 | Бюджет/деньги лида как стандартное поле? | Не нужно. Только через кастомные поля если требуется |
| 5 | Может ли consultant создавать лиды в любой воронке? | Нет. Только в воронках, разрешённых admin/sales_manager |

---

*Документ актуален на 2026-05-14. Версия 1.1 — все открытые вопросы закрыты.*
