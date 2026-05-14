# Source — Источник лидов

**Таблица:** `sources`  
**Статус:** Реализовано (Domain + Infrastructure + API)

---

## Описание

Источник определяет, откуда поступил лид: вручную, через webhook от внешней системы или через публичную форму. Каждый источник имеет тип и собственную конфигурацию в виде JSONB.

---

## Поля

| Поле | Тип БД | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, default uuid4 | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL | Название источника |
| `source_type` | VARCHAR(100) | NOT NULL, CHECK | Тип источника |
| `config` | JSONB | default={} | Конфигурация (зависит от типа) |
| `is_active` | BOOLEAN | default=true | Активен ли источник |
| `is_deleted` | BOOLEAN | default=false | Soft delete флаг |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL | Дата создания |
| `updated_at` | TIMESTAMP WITH TZ | NOT NULL | Дата последнего изменения |

---

## Типы источников (`source_type`)

### `manual` — Ручной ввод

Лид создаётся менеджером вручную через интерфейс.

```json
config: {}
```

---

### `webhook` — Вебхук

Внешняя система (сайт, бот, лендинг) отправляет POST-запрос, система автоматически создаёт лид.

```json
config: {
  "secret_token": "abc123xyz",
  "funnel_id": "uuid",
  "stage_id": "uuid",
  "field_mapping": {
    "name": "contact_name",
    "phone": "phone_number",
    "email": "email_address"
  }
}
```

| Поле конфига | Описание |
|---|---|
| `secret_token` | Bearer-токен для верификации запроса (заголовок `X-Webhook-Secret`) |
| `funnel_id` | Воронка, в которую попадёт лид |
| `stage_id` | Этап типа `initial`, на который попадёт лид |
| `field_mapping` | Маппинг: поле входящего JSON → поле лида |

---

### `public_form` — Публичная форма

Генерируется публичный URL; посетитель заполняет форму без авторизации.

```json
config: {
  "funnel_id": "uuid",
  "stage_id": "uuid",
  "visible_fields": ["name", "phone", "email", "comment"]
}
```

| Поле конфига | Описание |
|---|---|
| `funnel_id` | Воронка для входящих лидов |
| `stage_id` | Первый этап (`initial`) |
| `visible_fields` | Список полей, отображаемых на форме |

---

## Бизнес-правила

- Деактивированный источник (`is_active = false`) не принимает новые заявки
- Для `webhook`: при неверном `secret_token` возвращается `401`, событие логируется
- Для `webhook`: `secret_token` может быть перегенерирован — старый токен сразу становится невалидным
- Для `public_form`: URL формы `GET /forms/{source_id}` доступен без авторизации
- Только `admin` может создавать и удалять источники
- `admin` и `director` могут активировать/деактивировать

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| Lead.source_id → Source | Many-to-One | Каждый лид имеет источник |

---

## API эндпоинты

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| `GET` | `/api/v1/source/` | все | Список источников (фильтры: type, is_active) |
| `GET` | `/api/v1/source/{id}` | все | Получить источник |
| `POST` | `/api/v1/source/` | admin | Создать источник |
| `PUT` | `/api/v1/source/{id}` | admin | Обновить источник |
| `POST` | `/api/v1/source/{id}/activate` | admin, director | Активировать |
| `POST` | `/api/v1/source/{id}/deactivate` | admin, director | Деактивировать |
| `POST` | `/api/v1/source/{id}/regenerate-webhook-secret` | admin | Перегенерировать токен |
| `DELETE` | `/api/v1/source/{id}` | admin | Soft-delete источника |
| `POST` | `/webhook/{id}` | — (public) | Приём webhook, автосоздание лида |
| `GET` | `/forms/{id}` | — (public) | HTML публичной формы |
| `POST` | `/forms/{id}/submit` | — (public) | Отправка формы, создание лида |
