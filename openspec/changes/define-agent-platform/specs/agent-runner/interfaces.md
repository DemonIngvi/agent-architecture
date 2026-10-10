# agent-runner — конфигурация, данные, интерфейсы, отказы

← [spec.md](spec.md) · [схема](architecture.md) · [трассировка](traceability.md) · [правила](../../../../../docs/rules/spec-criteria.md)

## Уровни конфигурации

| Уровень | Что | Где хранится | Область |
|---|---|---|---|
| L0 | Конфиг деплоя | S9 | платформа целиком: адреса, переключатели G1–G4, режим планирования, потолки лимитов |
| L1 | Platform module | S2 | агент: бюджеты, профили, данные guardrails, флаги планирования |
| L2 | Определение агента | S1 (+ YAML импорт) | агент: модель, инструкция, тулы, навыки, MCP, лимиты запуска |
| L3 | Запуск | задача ICPlan / `Run` | версия агента, критерии приёмки, задание |

Правило: значение берётся с самого конкретного уровня (L3 → L0), но не выше потолка L0.

## Параметры модуля

| Параметр | Что задаёт | Уровень | Хранилище | По умолчанию |
|---|---|---|---|---|
| `poll_interval_ms` | Как часто опрашивать очередь | L0 | S9 | 3000 |
| `concurrency` | Параллельных запусков на агента | L1 | S2 | 1 |
| `timeout_s` | Таймаут запуска по умолчанию | L1 | S2 | 1800 |
| `retry` | Повтор при сбое инфраструктуры | L0 | S9 | 0 (без повтора) |
| `agents` | Ключи агентов, которые обслуживает Runner | L0 | S9 | — |
| `guardrails.g1.enabled` | Проверка допуска и бюджета | L0 | S9 | true |
| `scheduling.mode` | sequential или parallel | L0 | S9 | parallel |
| `scheduling.global_max` | Всего запусков одновременно | L0 | S9 | 4 |
| `scheduling.per_issue` | Запусков на задачу | L0 | S9 | 1 |
| `scheduling.order` | fifo или priority | L0 | S9 | fifo |
| `scheduling.agents.<id>.parallel / max` | Может ли агент идти в несколько потоков | L1 | S2 | по агенту |
| `scheduling.models.<alias>.max` | Запусков на модель | L0 | S9 | 3 |

## Хранилища данных

| ID | Хранилище | Что хранит | Владелец | Резервирование / срок |
|---|---|---|---|---|
| S2 | Postgres ICPlan, схема `platform` | настройки агентов, версии, профили sandbox и памяти, данные guardrails, параметры планирования | Platform module | вместе с S1 |
| S3 | Postgres ICPlan, схема `platform`, таблицы `run_event`, `scheduler_slot` | события запусков, слоты планировщика | Agent Runner / Observability | события — 90 дней; слоты — оперативные |
| S9 | Конфиг деплоя: `values.yaml` (git, без секретов) + Secret / `.env` (вне git) | параметры платформы, адреса, переключатели guardrails, секреты | эксплуатация | версии в git; секреты — вне git |

## Интерфейсы обмена

| ID | От → к | Протокол | Формат | Аутентификация | Режим | Таймаут | Повтор | Идемпотентность |
|---|---|---|---|---|---|---|---|---|
| I1 | ICPlan Run Queue → Agent Runner | HTTP REST (протокол `@itsaplan/runner`) | JSON `Run` | Bearer API-ключ агента | pull, опрос 3 с | 10 с | backoff до 60 с | аренда запуска: выдаётся одному Runner |
| I2 | Agent Runner → ICPlan (шаги, итог) | HTTP REST | JSON-пакеты `RunEvent` с `seq`, `RunResult` | Bearer API-ключ агента | асинхронно | 10 с | повтор с дедупликацией по (run_id, seq) | да, по (run_id, seq) |
| I3 | ICPlan → Agent Runner (approve, отмена) | HTTP REST, опрос состояния запуска | JSON `ApprovalDecision`, статус | Bearer API-ключ агента | pull | 10 с | backoff | да, по (run_id, seq) |
| I4 | Agent Runner → Platform module API | HTTP REST | JSON `AgentSettings` | сервисный токен | синхронно | 2 с | 3 раза | чтение |
| I5 | Agent Runner → OPA (G1) | HTTP REST `POST /v1/data/agent/g1` | JSON `PolicyInput` / `PolicyDecision` | внутренняя сеть (mTLS — позже) | синхронно | 200 мс | нет → `on_engine_error` | чтение |
| I6 | Agent Runner → Docker Engine API | HTTP поверх unix-сокета (позже K8s API) | JSON Docker API | доступ к сокету | синхронно | 30 с | 1 раз | create — нет; destroy — да |
| I7 | Agent Runner ↔ Harness | HTTP внутри сети sandbox; события — NDJSON-поток | `RunBundle`, `RunEvent`, `RunResult`, `ApprovalDecision` | одноразовый токен запуска | поток | = `timeout_s` | переподключение с последнего `seq` | да, по `seq` |
| I18 | Agent Runner → git-провайдер (токены) | HTTPS REST (GitHub App / Gitea API) | JSON | ключ приложения (Secret) | синхронно | 10 с | 2 раза | да |
| I19 | Agent Runner / ICPlan → MinIO | S3 API | файлы | ключи сервиса (Secret) | синхронно | 30 с | 3 раза | да, по ключу объекта |

Детали форматов — [потоки](../../../../../docs/flows/agent-runner.md).

## Отказы (FMEA)

| Отказ | Обнаружение | Поведение | Восстановление |
|---|---|---|---|
| ICPlan недоступен | ошибки I1 | опрос с backoff, активные запуски продолжаются, события буферизуются | досылка событий по `seq` |
| Platform module недоступен | ошибки I4 | новые запуски не стартуют (нет настроек) | повтор; кэш настроек не используется — безопасность |
| Docker / пул недоступен | ошибки I6 | запуск остаётся в `queued` | повтор, событие оператору |
| Runner упал | истечение аренды | запуски возвращаются в очередь, слоты освобождаются | новый экземпляр подхватывает |
| Нет настроек агента / ключа | пустой ответ I4 | запуск `agent_unavailable` | администратор заполняет настройки |
