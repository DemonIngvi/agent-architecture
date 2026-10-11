# Техспека: ICPlan (форк)

← [Все техспеки](README.md) · [компонент](../../components/icplan/index.md) · [правило](../rules/tech-spec.md)

**Что разворачивается:** web, api, worker, bot форка ICPlan с доработками платформы (модуль Platform, автоподхват, протокол раннера).

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| itsaplan-api | `oven/bun:1.4.0-alpine` (сборка) → `alpine:3.23` | API, миграции БД, MCP `itsaplan-core`, модули форка | Dockerfile `apps/api/Dockerfile` форка | `ghcr.io/demoningvi/itsaplan-api` (исходный — `ghcr.io/croffasia/itsaplan-api`) | версия форка | non-root | 3000 | `GET /health` |
| itsaplan-web | `oven/bun:1.4.0-alpine` → `node:24-alpine` | интерфейс (SSR) | `apps/web/Dockerfile` | `ghcr.io/demoningvi/itsaplan-web` | версия форка | non-root | 3001 | `GET /` |
| itsaplan-worker | `oven/bun:1.4.0-alpine` | фоновые задачи: уведомления, переходы процесса, очистка | `apps/worker/Dockerfile` | `ghcr.io/demoningvi/itsaplan-worker` | версия форка | non-root | — | процесс жив, очередь разбирается |
| itsaplan-bot | `oven/bun:1.4.0-alpine` | Telegram-бот | `apps/bot/Dockerfile` | `ghcr.io/demoningvi/itsaplan-bot` | версия форка | non-root | — | процесс жив |

## Запуск

| | |
|---|---|
| **Namespace** | `itsaplan-core` |
| **Реплики** | api 2, web 1–2, worker 1, bot 1 |
| **Запуск api** | `bun run packages/db/src/migrate.ts && bun run apps/api/src/index.ts` — миграции до старта |
| **Вход** | Traefik Ingress: web, api, `/mcp` |
| **Данные** | Postgres (CloudNativePG) через PgBouncer, RustFS (S3) |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `DATABASE_URL` | Postgres через PgBouncer (`prepare: false`) | Secret `itsaplan-db` |
| `S3_*` | RustFS | Secret `itsaplan-s3` |
| `AGENT_RUN_LEASE_SECONDS` | аренда запуска (300) | values |
| `TELEGRAM_BOT_TOKEN` | бот | Secret |

## Сборка и поставка

1. Форк: ветка `main` = upstream + модули с префиксом `platform_` и миграции форка
2. Сборка четырёх образов из `apps/*/Dockerfile` форка
3. Публикация в GHCR форка, чарт `itsaplan` с тегом форка
4. Сборка в GitHub Actions по тегу `vX.Y.Z` репозитория компонента; базовые образы закреплены по digest
5. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
6. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
7. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`; тег `latest` не используется
8. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] `/health` api = 200
- [ ] Вход в web
- [ ] Создать задачу и делегировать агенту → запуск в очереди

## Как работает {#how}

Порядок работы компонента: что за чем происходит внутри и с соседями. Поля данных — в [Модели данных](../../data-model.md), стороны и протоколы — в «Интеграциях» компонента, сквозной сценарий — в [архитектуре](../../architecture.md#interaction).

### Порядок работы


| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Пользователь двигает задачу по доске | Пользователь → Task UI | смена статуса задачи |
| 2 | Автоподхват: шаг процесса / Действие → агент-делегат | ICPlan → ICPlan | `delegateUserId` задачи |
| 3 | Постановка запуска в очередь | ICPlan → БД | `Run` (pending) |
| 4 | Runner забирает запуск | Agent Runner → ICPlan | `Run` |
| 5 | Ход работы агента в чат задачи | Agent Runner → ICPlan → браузер (SSE) | `RunEvent` (события AG-UI) → [чат запуска](#agent-feed) |
| 6 | Подтверждение действия | Пользователь → Task UI → Runner | `ApprovalDecision` |
| 7 | Итог в задачу | Agent Runner → ICPlan | `RunResult` → карточка итога в чате запуска; комментарии агент пишет сам тулом |
| 8 | Переход задачи по итогу запуска (по процессу; агент колонку не меняет) | ICPlan → ICPlan | `process_step.on_success / on_failure` |
| 9 | Администратор настраивает агента | Админ → Control Plane UI → Registry | `AgentDefinition` |

