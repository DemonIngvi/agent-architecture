# Deploy: ICPlan (форк)

← [компонент](../../components/icplan/index.md) · [методология](../rules/tech-spec.md)

**Что разворачивается:** web, api, worker, bot форка ICPlan с доработками платформы (модуль Platform, автоподхват, протокол раннера).

**Встроенные компоненты** (работают в образе `itsaplan-api`): [Platform module](platform-module.md) — модуль api; [Observability](observability.md) — в MVP без своего сервиса, события и сводка в ICPlan; [MCP itsaplan-core](mcp-tools.md) — `POST /mcp` (I24).

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| itsaplan-api | `oven/bun:1.4.0-alpine` (сборка) → `alpine:3.23`; теги upstream, digest закрепляется в CI форка | API, миграции БД, MCP `itsaplan-core`, модули форка | Dockerfile `apps/api/Dockerfile` форка | `ghcr.io/demoningvi/itsaplan-api` (исходный — `ghcr.io/croffasia/itsaplan-api`) | `vX.Y.Z` форка и `vX.Y.Z-<sha>` | non-root | 3000 | `GET /health` |
| itsaplan-web | `oven/bun:1.4.0-alpine` → `node:24-alpine`; digest — в CI форка | интерфейс (SSR) | `apps/web/Dockerfile` | `ghcr.io/demoningvi/itsaplan-web` | `vX.Y.Z` форка и `vX.Y.Z-<sha>` | non-root | 3001 | `GET /` |
| itsaplan-worker | `oven/bun:1.4.0-alpine`; digest — в CI форка | фоновые задачи: уведомления, переходы процесса, очистка | `apps/worker/Dockerfile` | `ghcr.io/demoningvi/itsaplan-worker` | `vX.Y.Z` форка и `vX.Y.Z-<sha>` | non-root | — | процесс жив, очередь разбирается |
| itsaplan-bot | `oven/bun:1.4.0-alpine`; digest — в CI форка | Telegram-бот | `apps/bot/Dockerfile` | `ghcr.io/demoningvi/itsaplan-bot` | `vX.Y.Z` форка и `vX.Y.Z-<sha>` | non-root | — | процесс жив |

## Запуск

| | |
|---|---|
| **Namespace** | `itsaplan-core` |
| **Реплики** | api 2, web 1–2, worker 1, bot 1 |
| **Запуск api** | `bun run packages/db/src/migrate.ts && bun run apps/api/src/index.ts` — миграции до старта |
| **Безопасность** | non-root, drop ALL capabilities, `no-new-privileges`, seccomp RuntimeDefault, read-only rootfs; запись — только во временный том `emptyDir` |
| **Вход** | Traefik Ingress: web, api, `/mcp` |
| **Данные** | Postgres (CloudNativePG) через PgBouncer, RustFS (S3) |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `DATABASE_URL` | Postgres через PgBouncer (`prepare: false`) | Secret `itsaplan-db` |
| `S3_*` | RustFS | Secret `itsaplan-s3` |
| `AGENT_RUN_LEASE_SECONDS` | аренда запуска; значение — [interfaces.md интеграции](../../openspec/changes/add-icplan-integration/specs/icplan-integration/interfaces.md) | values |
| `TELEGRAM_BOT_TOKEN` | бот | Secret |

## Сборка и поставка

1. Форк: ветка `main` = upstream + модули с префиксом `platform_` и миграции форка
2. Сборка четырёх образов из `apps/*/Dockerfile` форка в GitHub Actions по тегу `vX.Y.Z`; базовые образы закрепляются по digest
3. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
4. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
5. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`, чарт `itsaplan` с тегом форка; тег `latest` не используется
6. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] `/health` api = 200
- [ ] Вход в web
- [ ] Создать задачу и делегировать агенту → запуск в очереди
