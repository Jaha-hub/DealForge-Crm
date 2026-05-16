# План разработки Frontend — DealForge CRM

**Дата:** 2026-05-16  
**Стек:** Next.js 14 (App Router) · TypeScript · Tailwind CSS · shadcn/ui · Zustand · TanStack Query  
**Автор:** Frontend Developer

---

## Содержание

1. [Стек и инструменты](#1-стек-и-инструменты)
2. [Архитектура проекта](#2-архитектура-проекта)
3. [Структура папок](#3-структура-папок)
4. [Фазы разработки](#4-фазы-разработки)
5. [Экраны и маршруты](#5-экраны-и-маршруты)
6. [API-слой и типы](#6-api-слой-и-типы)
7. [State Management](#7-state-management)
8. [Auth и middleware](#8-auth-и-middleware)
9. [i18n (локализация)](#9-i18n-локализация)
10. [WebSocket (уведомления)](#10-websocket-уведомления)
11. [Checklist задач](#11-checklist-задач)

---

## 1. Стек и инструменты

| Категория | Инструмент | Зачем |
|---|---|---|
| Фреймворк | Next.js 14 (App Router) | SSR, layouts, server components |
| Язык | TypeScript 5 | Типизация |
| Стили | Tailwind CSS 3 | Утилитарные стили |
| UI-компоненты | shadcn/ui + Radix UI | Готовые accessible компоненты |
| Иконки | Lucide React | Консистентный набор иконок |
| Серверный стейт | TanStack Query v5 | Кэш, рефетч, мутации |
| Клиентский стейт | Zustand | UI-стейт, сессия |
| Формы | React Hook Form + Zod | Валидация + типизация форм |
| HTTP-клиент | Axios | Перехватчики, refresh token |
| DnD | @dnd-kit/core | Drag-and-drop Kanban-доски |
| Графики | Recharts | Аналитика (линейные, pie, bar) |
| i18n | next-intl | ru / uz / en |
| Уведомления | native WebSocket API | Подписка на события |
| Линтер | ESLint + Prettier | Код-стиль |
| Пакетный менеджер | pnpm | Быстрее npm/yarn |

---

## 2. Архитектура проекта

### Принципы

- **Feature-based структура** — каждая фича в своей папке (leads, funnels, analytics…)
- **Server Components** для страниц с fetch-данными, Client Components для интерактивных UI
- **Типы и схемы валидации** лежат рядом с фичей, не в общей папке types/
- **API-слой** полностью изолирован: компоненты не знают о fetch-логике напрямую

### Разделение компонентов

```
Server Component  →  Layout, страницы с начальными данными
Client Component  →  Kanban, формы, модалки, всё с useState/useEffect
```

### Роутинг (App Router)

```
/                          →  redirect → /dashboard
/(auth)/login              →  публичная
/(auth)/forgot-password    →  публичная
/(app)/dashboard           →  защищённая
/(app)/leads               →  защищённая
/(app)/leads/[id]          →  защищённая
/(app)/funnels             →  защищённая
/(app)/funnels/[id]        →  защищённая (Kanban)
/(app)/sources             →  защищённая
/(app)/custom-fields       →  защищённая
/(app)/analytics           →  защищённая
/(app)/users               →  только admin
/(app)/profile             →  защищённая
/forms/[source_id]         →  публичная (без auth)
/forms/[source_id]/success →  публичная
```

---

## 3. Структура папок

```
frontend/
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── (auth)/                  # Группа: публичные страницы
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── (app)/                   # Группа: защищённые страницы
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── leads/
│   │   │   │   ├── page.tsx         # Список лидов
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx     # Карточка лида
│   │   │   ├── funnels/
│   │   │   │   ├── page.tsx         # Список воронок
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx     # Kanban-доска
│   │   │   ├── sources/
│   │   │   │   └── page.tsx
│   │   │   ├── custom-fields/
│   │   │   │   └── page.tsx
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx
│   │   │   ├── users/
│   │   │   │   └── page.tsx
│   │   │   ├── profile/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx           # AppShell (сайдбар + хедер)
│   │   ├── forms/
│   │   │   └── [source_id]/
│   │   │       ├── page.tsx         # Публичная форма
│   │   │       └── success/
│   │   │           └── page.tsx
│   │   ├── layout.tsx               # Root layout (провайдеры)
│   │   └── not-found.tsx
│   │
│   ├── features/                    # Фичи приложения
│   │   ├── auth/
│   │   │   ├── api.ts               # login, refresh, logout
│   │   │   ├── hooks.ts             # useLogin, useLogout
│   │   │   ├── schemas.ts           # Zod-схемы
│   │   │   └── components/
│   │   │       └── LoginForm.tsx
│   │   ├── leads/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   ├── schemas.ts
│   │   │   ├── types.ts
│   │   │   └── components/
│   │   │       ├── LeadCard.tsx
│   │   │       ├── LeadTable.tsx
│   │   │       ├── LeadForm.tsx
│   │   │       ├── LeadFilters.tsx
│   │   │       └── LeadHistory.tsx
│   │   ├── kanban/
│   │   │   ├── hooks.ts
│   │   │   └── components/
│   │   │       ├── KanbanBoard.tsx
│   │   │       ├── KanbanColumn.tsx
│   │   │       └── KanbanCard.tsx
│   │   ├── funnels/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   ├── types.ts
│   │   │   └── components/
│   │   │       ├── FunnelList.tsx
│   │   │       ├── FunnelForm.tsx
│   │   │       └── StageForm.tsx
│   │   ├── sources/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   ├── types.ts
│   │   │   └── components/
│   │   │       ├── SourceList.tsx
│   │   │       ├── SourceForm.tsx
│   │   │       ├── WebhookKeyCard.tsx
│   │   │       └── EmbedCodeCard.tsx
│   │   ├── custom-fields/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   ├── types.ts
│   │   │   └── components/
│   │   │       ├── CustomFieldList.tsx
│   │   │       ├── CustomFieldForm.tsx
│   │   │       └── EnumEditor.tsx
│   │   ├── analytics/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   └── components/
│   │   │       ├── DashboardWidgets.tsx
│   │   │       ├── FunnelChart.tsx
│   │   │       ├── SourcesChart.tsx
│   │   │       ├── ManagersTable.tsx
│   │   │       └── DynamicsChart.tsx
│   │   ├── notifications/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts             # useNotifications, useWebSocket
│   │   │   └── components/
│   │   │       ├── NotificationBell.tsx
│   │   │       └── NotificationList.tsx
│   │   ├── users/
│   │   │   ├── api.ts
│   │   │   ├── hooks.ts
│   │   │   └── components/
│   │   │       ├── UserTable.tsx
│   │   │       └── UserForm.tsx
│   │   └── public-form/
│   │       ├── api.ts
│   │       └── components/
│   │           ├── PublicFormRenderer.tsx
│   │           └── SuccessPage.tsx
│   │
│   ├── components/                  # Переиспользуемые UI-компоненты
│   │   ├── ui/                      # shadcn/ui компоненты (генерируются)
│   │   ├── layout/
│   │   │   ├── AppShell.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Header.tsx
│   │   └── shared/
│   │       ├── PageHeader.tsx
│   │       ├── ConfirmDialog.tsx
│   │       ├── EmptyState.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── RoleBadge.tsx
│   │
│   ├── lib/
│   │   ├── axios.ts                 # Axios instance + interceptors
│   │   ├── query-client.ts          # TanStack Query config
│   │   └── utils.ts                 # cn(), formatDate(), formatCurrency()
│   │
│   ├── store/
│   │   ├── auth.store.ts            # Zustand: user, tokens, role
│   │   └── ui.store.ts              # Zustand: sidebarOpen, activeFunnel
│   │
│   ├── middleware.ts                # Next.js middleware — защита роутов
│   │
│   └── i18n/
│       ├── request.ts
│       ├── routing.ts
│       └── messages/
│           ├── ru.json
│           ├── uz.json
│           └── en.json
│
├── public/
├── .env.local
├── next.config.ts
├── tailwind.config.ts
├── components.json                  # shadcn/ui config
└── package.json
```

---

## 4. Фазы разработки

### Фаза 0 — Настройка проекта (1–2 дня)

- [ ] Инициализация Next.js 14 с TypeScript
- [ ] Tailwind CSS + shadcn/ui (init, компоненты: Button, Input, Dialog, Table, Tabs, Badge, Select, Textarea, Card, Dropdown, Toast)
- [ ] Настройка pnpm, ESLint, Prettier
- [ ] Axios instance с interceptors (refresh token)
- [ ] TanStack Query provider
- [ ] Zustand-сторы (auth, ui)
- [ ] next-intl для i18n (ru/uz/en)
- [ ] Middleware защиты роутов
- [ ] `.env.local` с `NEXT_PUBLIC_API_URL`

---

### Фаза 1 — Auth + AppShell (2–3 дня)

**Экраны:**
- Login page (`/login`)
- AppShell: сайдбар + хедер + layout

**Детали:**
- Форма логина: email + password, валидация Zod
- JWT: access token в памяти (Zustand), refresh token в httpOnly cookie
- Interceptor: при 401 → автоматический refresh → retry запроса
- Хедер: имя пользователя, роль, кнопка выхода, бел уведомлений
- Сайдбар: навигация с учётом роли (admin видит Users, consultant не видит Analytics)
- Мобильная: сайдбар скрывается в burger-меню

---

### Фаза 2 — Kanban-доска (3–4 дня)

**Экран:** `/funnels/[id]` — главный рабочий экран

**Детали:**
- Список воронок в верхней части (табы или dropdown)
- Колонки = этапы воронки (`initial → intermediate → won/lost`)
- Карточки лидов: имя, телефон, источник, дата создания, назначенный менеджер
- Drag-and-drop (@dnd-kit): перетаскивание карточки между колонками → `PATCH /leads/{id}/stage`
- При переводе в `won`/`lost` — диалог подтверждения
- Быстрое создание лида прямо с Kanban: кнопка «+» в колонке
- Счётчик лидов на каждой колонке

---

### Фаза 3 — Список лидов + Карточка лида (3–4 дня)

**Экраны:** `/leads` и `/leads/[id]`

**Список лидов:**
- Таблица: имя, телефон, воронка, этап, источник, менеджер, дата
- Фильтры: воронка, этап, источник, ответственный, теги, период (created_at)
- Сортировка по столбцам
- Пагинация (или infinite scroll)
- Быстрое действие: удалить, изменить этап

**Карточка лида:**
- Шапка: имя, теги, статус (этап), дата создания
- Редактирование inline (клик → поле редактируется)
- Блок стандартных полей: телефон, email, комментарий, источник
- Блок кастомных полей (рендер по типу: text, number, date, select_one, select_many, boolean)
- Назначение менеджера: dropdown с поиском
- История изменений (`GET /leads/{id}/history`): хронологический лог

---

### Фаза 4 — Управление воронками (2–3 дня)

**Экраны:** `/funnels`

**Список воронок:**
- Карточки воронок: название, количество этапов, количество лидов
- Создать / переименовать / удалить воронку

**Редактор этапов (внутри воронки):**
- Список этапов с drag-and-drop для изменения порядка
- Для каждого этапа: название, цвет (color picker), тип (initial/intermediate/won/lost), вероятность 0–100%
- Добавить / удалить / изменить этап

---

### Фаза 5 — Источники лидов (2 дня)

**Экран:** `/sources`

**Список источников:**
- Таблица: имя, тип (manual/webhook/public_form), статус, дата создания
- Фильтр по типу и статусу
- Активировать / деактивировать

**Форма создания/редактирования источника:**
- Название + выбор типа
- Для `webhook`: отображение секретного ключа + кнопка «Регенерировать»
- Для `public_form`: embed-код (`<iframe>`) + кнопка копирования + ссылка на форму
- Для `webhook`/`public_form`: выбор воронки, к которой привязан источник

---

### Фаза 6 — Кастомные поля (2 дня)

**Экран:** `/custom-fields`

**Список полей:**
- Таблица: название, тип, обязательное, количество значений (для enum)
- Создать / переименовать / удалить (soft)

**Редактор полей:**
- Выбор типа поля (text, number, date, time, select_one, select_many, boolean)
- Для `select_one` / `select_many`: редактор enum-значений (добавить / удалить значение)
- Предпросмотр поля

---

### Фаза 7 — Аналитика (3–4 дня)

**Экран:** `/analytics` — вкладки

**Вкладка: Дашборд**
- 4 виджета: всего лидов, конверсия %, открытые лиды, pie-chart по источникам
- Фильтр по периоду

**Вкладка: Воронка**
- Bar chart: лиды на каждом этапе
- Конверсия между этапами (%)
- Среднее время на этапе
- Фильтры: воронка, период, менеджер

**Вкладка: Источники**
- Таблица + bar chart: лиды по источникам
- Конверсия в `won` по источнику

**Вкладка: Менеджеры**
- Таблица: менеджер → лиды → won → конверсия → среднее время закрытия
- Фильтр по периоду

**Вкладка: Динамика**
- Line chart: новые лиды + закрытые сделки по датам
- Выбор периода: вчера / неделя / месяц / квартал / произвольный

---

### Фаза 8 — Уведомления WebSocket (2 дня)

**Компонент:** `NotificationBell` в хедере

**Детали:**
- WebSocket-соединение: `ws://api/ws/notifications` (с JWT токеном в query params)
- При открытии WS → загрузка непрочитанных уведомлений
- Новые события приходят push-сообщением → добавляются в список
- Счётчик непрочитанных (badge на колоколе)
- Дропдаун со списком: иконка, заголовок, время
- «Прочитать всё» одной кнопкой
- Переподключение при разрыве (exponential backoff)

---

### Фаза 9 — Пользователи и профиль (1–2 дня)

**Экран `/users`** (только `admin`):
- Таблица пользователей: имя, email, роль, статус
- Создать пользователя: имя, email, пароль, роль
- Изменить роль
- Деактивировать / активировать

**Экран `/profile`:**
- Имя, email (только просмотр)
- Смена пароля: текущий + новый + подтверждение
- Выбор языка интерфейса (ru / uz / en)

---

### Фаза 10 — Публичная форма (1–2 дня)

**Экраны:** `/forms/[source_id]` и `/forms/[source_id]/success`

**Детали:**
- Без авторизации, отдельный layout (без AppShell)
- Рендер полей по конфигурации источника (стандартные + кастомные)
- Валидация на клиенте (Zod)
- `POST /forms/{source_id}/submit` при отправке
- Редирект на `/forms/[source_id]/success` после успеха
- Брендинг: название компании / логотип из конфига источника

---

## 5. Экраны и маршруты

| Маршрут | Компонент | Auth | Роли |
|---|---|---|---|
| `/login` | LoginPage | Нет | Все |
| `/dashboard` | DashboardPage | Да | Все |
| `/funnels` | FunnelListPage | Да | admin, director, sales_manager |
| `/funnels/[id]` | KanbanPage | Да | Все |
| `/leads` | LeadListPage | Да | Все |
| `/leads/[id]` | LeadDetailPage | Да | Все |
| `/sources` | SourcesPage | Да | admin, director |
| `/custom-fields` | CustomFieldsPage | Да | admin, director |
| `/analytics` | AnalyticsPage | Да | admin, director, sales_manager |
| `/users` | UsersPage | Да | admin |
| `/profile` | ProfilePage | Да | Все |
| `/forms/[source_id]` | PublicFormPage | Нет | Публичная |
| `/forms/[source_id]/success` | SuccessPage | Нет | Публичная |

---

## 6. API-слой и типы

### Axios instance (`lib/axios.ts`)

```typescript
// Базовый URL из env
// Interceptor request: добавить Authorization: Bearer {accessToken}
// Interceptor response: при 401 → POST /auth/refresh → retry
// При неудаче refresh → logout + redirect /login
```

### Структура API-модуля (пример: `features/leads/api.ts`)

```typescript
export const leadsApi = {
  list: (params: LeadFilters) => axios.get('/leads/', { params }),
  get: (id: string) => axios.get(`/leads/${id}`),
  create: (data: CreateLeadDto) => axios.post('/leads/', data),
  update: (id: string, data: UpdateLeadDto) => axios.put(`/leads/${id}`, data),
  delete: (id: string) => axios.delete(`/leads/${id}`),
  changeStage: (id: string, stageId: string) => axios.patch(`/leads/${id}/stage`, { stage_id: stageId }),
  assign: (id: string, userId: string) => axios.patch(`/leads/${id}/assign`, { assign_to: userId }),
  history: (id: string) => axios.get(`/leads/${id}/history`),
}
```

### Типы (пример: `features/leads/types.ts`)

```typescript
export type LeadStatus = 'initial' | 'intermediate' | 'won' | 'lost'

export interface Lead {
  id: string
  name: string
  phone?: string
  email?: string
  comment?: string
  tags: string[]
  source_id: string
  funnel_id: string
  stage_id: string
  assign_to?: string
  custom_values: LeadCustomFieldValue[]
  is_deleted: boolean
  closed_at?: string
  created_at: string
  updated_at: string
}
```

---

## 7. State Management

### Zustand — только клиентский UI-стейт

```typescript
// store/auth.store.ts
interface AuthStore {
  user: User | null
  accessToken: string | null
  setUser: (user: User) => void
  setToken: (token: string) => void
  logout: () => void
}

// store/ui.store.ts
interface UIStore {
  sidebarOpen: boolean
  activeFunnelId: string | null
  toggleSidebar: () => void
  setActiveFunnel: (id: string) => void
}
```

### TanStack Query — серверный стейт

```typescript
// features/leads/hooks.ts
export const useLeads = (filters: LeadFilters) =>
  useQuery({ queryKey: ['leads', filters], queryFn: () => leadsApi.list(filters) })

export const useCreateLead = () =>
  useMutation({
    mutationFn: leadsApi.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
  })
```

**Ключи кэша TanStack Query:**
- `['leads', filters]` — список лидов
- `['lead', id]` — один лид
- `['funnels']` — воронки
- `['funnel', id]` — одна воронка со стадиями
- `['sources']` — источники
- `['custom-fields']` — кастомные поля
- `['analytics', 'dashboard', period]` — дашборд
- `['analytics', 'funnel', funnelId, filters]` — аналитика воронки
- `['notifications']` — уведомления
- `['users']` — список пользователей

---

## 8. Auth и middleware

### Стратегия токенов

- `accessToken` — в памяти (Zustand, 2 часа)
- `refreshToken` — в httpOnly cookie (7 дней, устанавливается backend)
- При F5/перезагрузке: Axios делает `POST /auth/refresh` автоматически

### Middleware (`middleware.ts`)

```typescript
// Если нет access token и нет refresh cookie → redirect /login
// Если роль не соответствует маршруту → redirect /dashboard
// Публичные роуты: /login, /forms/*
```

### Защита по ролям на клиенте

Компонент-обёртка `RoleGuard`:
```tsx
<RoleGuard allow={['admin', 'director']}>
  <UsersPage />
</RoleGuard>
```

---

## 9. i18n (локализация)

- Библиотека: `next-intl`
- Языки: `ru` (по умолчанию), `uz`, `en`
- Locale хранится в профиле пользователя, синхронизируется в cookie
- Дата/время: `UTC+5` (Ташкент), через `Intl.DateTimeFormat`
- Валюта: UZS

**Структура переводов:**

```json
// i18n/messages/ru.json
{
  "nav": { "dashboard": "Дашборд", "leads": "Лиды", ... },
  "leads": { "create": "Создать лид", "name": "Имя", ... },
  "analytics": { "conversion": "Конверсия", ... }
}
```

---

## 10. WebSocket (уведомления)

```typescript
// features/notifications/hooks.ts

export const useNotificationsSocket = () => {
  const { accessToken } = useAuthStore()

  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/ws/notifications?token=${accessToken}`)

    ws.onmessage = (event) => {
      const notification = JSON.parse(event.data)
      // добавить в Zustand или инвалидировать TanStack Query
      queryClient.setQueryData(['notifications'], (old) => [notification, ...old])
    }

    ws.onclose = () => {
      // reconnect с exponential backoff
    }

    return () => ws.close()
  }, [accessToken])
}
```

---

## 11. Checklist задач

### Фаза 0 — Настройка
- [ ] `pnpm create next-app` с TypeScript
- [ ] Установить Tailwind CSS
- [ ] Установить shadcn/ui, инициализировать, добавить компоненты
- [ ] Установить: `axios`, `@tanstack/react-query`, `zustand`, `react-hook-form`, `zod`, `next-intl`, `@dnd-kit/core @dnd-kit/sortable`, `recharts`, `lucide-react`
- [ ] Настроить ESLint + Prettier
- [ ] Создать `lib/axios.ts` с interceptors
- [ ] Создать `lib/query-client.ts`
- [ ] Создать `store/auth.store.ts` и `store/ui.store.ts`
- [ ] Создать root layout с провайдерами
- [ ] Написать `middleware.ts`
- [ ] Создать `.env.local` (`NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_WS_URL`)

### Фаза 1 — Auth + AppShell
- [ ] LoginForm (react-hook-form + zod)
- [ ] `useLogin` мутация, сохранение токена
- [ ] AppShell layout: Sidebar + Header
- [ ] Sidebar: навигация с учётом ролей
- [ ] Адаптивный сайдбар (mobile burger)

### Фаза 2 — Kanban
- [ ] `KanbanBoard` с @dnd-kit
- [ ] `KanbanColumn` (этап) + `KanbanCard` (лид)
- [ ] DnD → `PATCH /leads/{id}/stage`
- [ ] Диалог подтверждения при won/lost
- [ ] Быстрое создание лида из колонки

### Фаза 3 — Leads
- [ ] `LeadTable` с фильтрами и пагинацией
- [ ] `LeadDetail` страница
- [ ] Inline-редактирование полей
- [ ] Рендер кастомных полей по типу
- [ ] Назначение менеджера
- [ ] `LeadHistory` компонент

### Фаза 4 — Funnels
- [ ] Список воронок
- [ ] CRUD воронки
- [ ] Редактор этапов с DnD-сортировкой
- [ ] Color picker для этапа

### Фаза 5 — Sources
- [ ] Список источников с фильтрами
- [ ] Форма создания (3 типа)
- [ ] Webhook key display + regenerate
- [ ] Embed code + copy

### Фаза 6 — Custom Fields
- [ ] Список полей
- [ ] Форма создания поля (выбор типа)
- [ ] EnumEditor (добавить/удалить значения)

### Фаза 7 — Analytics
- [ ] DashboardWidgets (4 виджета)
- [ ] FunnelChart (bar chart этапов)
- [ ] SourcesChart (bar + таблица)
- [ ] ManagersTable
- [ ] DynamicsChart (line chart)
- [ ] Фильтры по периоду (date range picker)

### Фаза 8 — Notifications
- [ ] `useNotificationsSocket` hook
- [ ] `NotificationBell` с badge
- [ ] Дропдаун со списком
- [ ] Read / Read All действия
- [ ] Reconnect логика

### Фаза 9 — Users + Profile
- [ ] UserTable (только admin)
- [ ] UserForm (создать/изменить роль)
- [ ] ProfilePage (смена пароля, язык)

### Фаза 10 — Public Form
- [ ] `PublicFormRenderer` (рендер полей по конфигу)
- [ ] Валидация + submit
- [ ] SuccessPage

---

## Приоритеты (порядок реализации)

```
Фаза 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10
```

Фаза 2 (Kanban) — приоритет сразу после Auth, это ключевой рабочий экран.  
Фаза 7 (Analytics) — зависит от готовности backend-эндпоинтов.  
Фаза 10 (Public Form) — независима, можно делать параллельно.

---

*Документ актуален на 2026-05-16. Обновляется по мере изменений в PRD.*
