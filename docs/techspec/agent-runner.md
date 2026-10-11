# Техспека: Agent Runner

← [Все техспеки](README.md) · [компонент](../../components/agent-runner/index.md) · [правило](../rules/tech-spec.md)

**Что разворачивается:** Go-сервис: забирает запуски из ICPlan, планирует слоты, поднимает sandbox, связывает с Harness.

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| agent-runner | `golang:1.2x` (сборка) → `gcr.io/distroless/static:nonroot` | статический бинарник Runner | `runner/Dockerfile` репозитория платформы | `ghcr.io/demoningvi/agent-runner` | semver платформы | nonroot (65532) | 8080 (метрики, health) | `GET /healthz`, `GET /readyz` (ICPlan и Platform module доступны) |

## Запуск

| | |
|---|---|
| **Namespace** | `itsaplan-agents` |
| **Реплики** | 1 (MVP), 2 — с общими слотами |
| **Доступ к контейнерам** | этапы 1–3: rootless Docker на узле (сокет пользователя Runner); этап 4: ServiceAccount на `itsaplan-agents` (I23) |
| **Ресурсы** | requests 0.1 CPU / 128 МиБ, limits 0.5 / 512 МиБ |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `ITSAPLAN_URL`, `ITSAPLAN_AGENT_KEYS` | очередь и ключи агентов | Secret `runner-agents` |
| `PLATFORM_API_URL`, `PLATFORM_TOKEN` | настройки агентов | Secret |
| `DOCKER_HOST` | rootless Docker | values |
| `HARNESS_IMAGE` | образ sandbox | values |
| секреты MCP-серверов (`auth.secret_ref`) | MCP-прокси подставляет учётные данные (D19) | Secret в `itsaplan-agents`, чтение — ServiceAccount Runner |
| `SETUP_NETWORK` | сеть шага подготовки `sbx-setup` | values |

## Сборка и поставка

1. Сборка в GitHub Actions по тегу `vX.Y.Z` репозитория компонента; базовые образы закреплены по digest
2. `CGO_ENABLED=0 go build -trimpath -ldflags='-s -w'`
3. Копирование бинарника в distroless
4. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
5. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
6. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`; тег `latest` не используется
7. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] Runner «в сети» в ICPlan
- [ ] Тестовый запуск на mock-LLM доходит до итога

## Как работает {#how}

Порядок работы компонента: что за чем происходит внутри и с соседями. Поля данных — в [Модели данных](../../data-model.md), стороны и протоколы — в «Интеграциях» компонента, сквозной сценарий — в [архитектуре](../../architecture.md#interaction).

### Порядок работы


| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Опрос очереди по ключу агента | Runner → ICPlan | `Run` |
| 2 | Планирование: свободны ли слоты (глобальный, агента, модели, задачи) | Runner → таблица слотов | `queued` → `admitted` |
| 2a | Допуск, бюджет (G1) | Runner → OPA | `PolicyInput` → `PolicyDecision` |
| 3 | Профиль и бюджет агента | Runner → Platform module | `AgentSettings` |
| 4 | Контейнер из тёплого пула | Runner → Sandbox | `profile` → `sandboxId` |
| 5 | Токен репозиториев на запуск | Runner → git-провайдер | `RepoGrant` |
| 6 | Задание для Harness | Runner → Harness | `RunBundle` |
| 7 | События шагов | Harness → Runner → ICPlan | `RunEvent` |
| 8 | Решение по паузе | ICPlan → Runner → Harness | `ApprovalDecision` |
| 9 | Итог | Harness → Runner → ICPlan | `RunResult` |
| 10 | Таймаут или отмена | Runner → Harness | сигнал остановки |
| 11 | Уничтожение контейнера, долив пула | Runner → Sandbox | `sandboxId` |

### Состояния запуска


Единый список статусов запуска — требование R-RUN-07; остальные документы ссылаются на него.

```
queued ─▶ starting ─▶ running ─▶ succeeded
  │  (ждёт слот)          ├──────▶ waiting_approval ─▶ running
  │                       ├──────▶ gate_failed
  │                       ├──────▶ limit_exceeded   (шаги, время, простой, бюджет, зацикливание)
  │                       ├──────▶ failed
  │                       └──────▶ canceled
  └─▶ limit_exceeded / failed   (G1 до старта: бюджет / kill switch, агент недоступен)
```

| Причина завершения Harness (R-HRN-09) | Статус запуска (R-RUN-07) | Статус в ICPlan (`agent_run`) |
|---|---|---|
| `done` | `succeeded` | `success` |
| `gate_failed` | `gate_failed` | `failed` с пометкой «не прошёл проверку» |
| `limit` (шаги, время, простой, `loop_detected`) | `limit_exceeded` | `failed` с причиной |
| `error` | `failed` | `failed` |
| остановка пользователем | `canceled` | `canceled` |

