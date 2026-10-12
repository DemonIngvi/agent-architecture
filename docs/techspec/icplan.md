# Deploy: ICPlan (форк)

← [компонент](../../components/icplan/index.md) · [методология](../rules/tech-spec.md)

**Что разворачивается:** web, api, worker, bot форка ICPlan с доработками платформы (модуль Platform, автоподхват, протокол раннера). Развёртывание — чарт форка `charts/itsaplan`; «как в форке» сверено с кодом `DemonIngvi/itsaplan-app` (12.10.2026), «нужно» — доработка в [задаче 4.6](../tasks/4.6-k8s-helm-ingress.md).

**Встроенные компоненты** (работают в образе api): [Platform module](platform-module.md) — модуль api; [Observability](observability.md) — в MVP без своего сервиса, события и сводка в ICPlan; [MCP itsaplan-core](mcp-tools.md) — `POST /mcp` (I24).

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| api | `oven/bun:1.4.0-alpine` (сборка) → `alpine:3.23` | API, миграции БД (`packages/db`), MCP `itsaplan-core`, модули платформы; `bun install --frozen-lockfile` по `bun.lock`; клиент `postgresql18-client` для дампа перед миграцией | `apps/api/Dockerfile` | `ghcr.io/demoningvi/itsaplan-app-api` | см. «Сборка и поставка» | **как в форке:** в Dockerfile нет `USER` — root; **нужно:** non-root через `securityContext` чарта (ниже) | 3000 | `GET /health` |
| web | `oven/bun:1.4.0-alpine` → `node:24-alpine` | интерфейс (SSR) | `apps/web/Dockerfile` | `ghcr.io/demoningvi/itsaplan-app-web` | см. ниже | как api | 3001 | `GET /` |
| worker | `oven/bun:1.4.0-alpine` | фоновые задачи: уведомления, переходы процесса, очистка | `apps/worker/Dockerfile` | `ghcr.io/demoningvi/itsaplan-app-worker` | см. ниже | как api | — | процесс жив, очередь разбирается |
| bot | `oven/bun:1.4.0-alpine` | Telegram-бот | `apps/bot/Dockerfile` | `ghcr.io/demoningvi/itsaplan-app-bot` | см. ниже | как api | — | процесс жив |

Версия форка: `X.Y.Z` форка ведёт release-please форка; версия upstream, на которой основан выпуск, — в описании выпуска форка.

## Запуск

| | |
|---|---|
| **Namespace** | `itsaplan-core` |
| **Реплики** | api 2, web 1–2, worker 1, bot 1 |
| **Миграции** | init-контейнер `migrate` чарта (`bun run packages/db/src/migrate.ts`) до старта api; реплики ждут друг друга на `pg_advisory_lock`. **Как в форке:** init-контейнер берёт тот же `DATABASE_URL`; **нужно:** для `migrate` — прямое подключение к Postgres (сервис `-rw` CloudNativePG), минуя PgBouncer: в режиме transaction сессионная блокировка ненадёжна |
| **Дамп перед миграцией** | init-контейнер снимает дамп в `/backups`. **Как в форке:** `api.backups.persistence.enabled: false` → дамп в `emptyDir` и пропадает с подом; **нужно:** `api.backups.persistence` (PVC) **или** `SKIP_PRE_MIGRATION_BACKUP=1` при бэкапе CloudNativePG (PITR) |
| **Безопасность** | **как в форке:** `podSecurityContext: {}`, `securityContext: {}`; **нужно (values):** `podSecurityContext: {runAsNonRoot: true, runAsUser: 1000, fsGroup: 1000}`, `securityContext: {allowPrivilegeEscalation: false, capabilities: {drop: [ALL]}, readOnlyRootFilesystem: true, seccompProfile: {type: RuntimeDefault}}`; запись — только `emptyDir` и том дампа |
| **Вход** | Traefik Ingress: web, api, `/mcp` |
| **Данные** | Postgres (CloudNativePG) через PgBouncer, RustFS (S3) — [базы и роли](../../data-by-component/infrastructure/index.md#databases) |

## Переменные и секреты

Инвентаризация по `.env.example` и `values.yaml` форка.

| Переменная | Зачем | Откуда |
|---|---|---|
| `DATABASE_URL` | база `itsaplan`, роль `itsaplan` — схемы `public` и `platform` (Platform module, Observability), через PgBouncer (`prepare: false`); D22 | Secret `itsaplan-db` |
| `MIGRATION_DATABASE_URL` (нужно) | прямое подключение к Postgres для init-контейнера `migrate` | Secret `itsaplan-db` |
| `LITELLM_READ_URL` | база `litellm`, роль `litellm_read` — чтение журнала затрат (Observability); D22 | Secret `litellm-read` |
| `APP_ENCRYPTION_KEY` | шифрует секреты в БД (ключи агентов `ai_agent.api_key_ciphertext`, учётные данные тулов); без него данные из бэкапа не прочитать — хранится вместе с планом восстановления | Secret |
| `BETTER_AUTH_SECRET` | подпись сессий пользователей | Secret |
| `API_URL`, `APP_URL` | адреса api и web | values |
| `S3_*` | RustFS: бакет, регион, path-style | Secret `itsaplan-s3`, values |
| `SSRF_ALLOWED_HOSTS` | внутренние хосты, к которым api можно обращаться (например, LiteLLM, Memory API) | values |
| `TELEMETRY_DISABLED` | `"1"` — телеметрия upstream выключена (в `values.yaml` форка уже стоит для api и worker) | values |
| `SKIP_PRE_MIGRATION_BACKUP` | `1`, если дамп перед миграцией не нужен (бэкап CloudNativePG) | values |
| `AGENT_RUN_LEASE_SECONDS` | аренда запуска; значение — [interfaces.md интеграции](../../openspec/changes/add-icplan-integration/specs/icplan-integration/interfaces.md) | values |
| `AGENT_RUN_RETENTION_DAYS` (нужно) | worker: срок завершённых запусков `agent_run` — параметр `runs.retention_days`; 0 — не чистить; задача очистки по образцу `cleanupOldDeliveries` / `WEBHOOK_CLEANUP_DAYS` (R-ICP-19, D25); значение — [interfaces.md интеграции](../../openspec/changes/add-icplan-integration/specs/icplan-integration/interfaces.md) | values |
| `AGENT_CHAT_RETENTION_DAYS` (нужно) | worker: срок тредов чата агента — параметр `chat.retention_days`; 0 — не чистить (R-ICP-19, D25) | values |
| `TELEGRAM_BOT_TOKEN` | бот | Secret |

## Сборка и поставка

| Шаг | Как в форке (`.github/workflows`) | Нужно (задача 4.6) |
|---|---|---|
| 1. Код | ветка `main` = upstream + модули `platform_` и миграции форка | — |
| 2. Проверки | `ci.yml`: jobs `quality`, `build`, `test` на push | обязательны перед публикацией |
| 3. Сборка | `publish-images.yml`: четыре образа из `apps/*/Dockerfile`, многостадийно | базы — по digest |
| 4. SBOM и уязвимости | нет | `syft` (SBOM), `trivy` — выпуск блокируется при critical |
| 5. Публикация | `ghcr.io/demoningvi/itsaplan-app-<service>:X.Y.Z`; без суффикса пред-релиза двигается `latest`; тега с sha нет | `X.Y.Z` и `X.Y.Z-<sha>`; `latest` не используется |
| 6. Доставка | чарт `charts/itsaplan` | кластер тянет образы с pull-секретом `ghcr-pull` |

## Пример конфигурации

Значения — по `charts/itsaplan/values.yaml` форка и `interfaces.md` спек; новых значений здесь нет.

```yaml
podSecurityContext: { runAsNonRoot: true, runAsUser: 1000, fsGroup: 1000 }
securityContext:
  allowPrivilegeEscalation: false
  capabilities: { drop: [ALL] }
  readOnlyRootFilesystem: true
  seccompProfile: { type: RuntimeDefault }
api:
  replicaCount: 2
  env: { TELEMETRY_DISABLED: "1", SSRF_ALLOWED_HOSTS: "<хосты LiteLLM и Memory API в кластере>" }
  backups: { persistence: { enabled: true, size: 10Gi } }   # или SKIP_PRE_MIGRATION_BACKUP=1 при PITR CloudNativePG
worker:
  env: { TELEMETRY_DISABLED: "1", AGENT_RUN_RETENTION_DAYS: "365", AGENT_CHAT_RETENTION_DAYS: "90" }   # runs.retention_days, chat.retention_days (D25)
```

## Обновление и откат

1. Перед `helm upgrade` — точка восстановления: дамп init-контейнера (если включён) или отметка времени для PITR CloudNativePG.
2. `helm upgrade`: init-контейнер `migrate` применяет миграции (только вперёд), затем стартуют api.
3. Откат образа без миграций — `helm rollback`.
4. Откат после миграции — `helm rollback` + восстановление базы из дампа перед миграцией или PITR на отметку шага 1; вложения RustFS не откатываются: восстановленная база может ссылаться на файлы, загруженные позже, — они остаются, недостающих нет.
5. Ключ `APP_ENCRYPTION_KEY` не меняется при откате: без того же ключа зашифрованные данные не читаются.

## Проверка после развёртывания

- [ ] `/health` api = 200
- [ ] Вход в web
- [ ] Создать задачу и делегировать агенту → запуск в очереди
- [ ] Поды запущены не от root (`runAsNonRoot`)
