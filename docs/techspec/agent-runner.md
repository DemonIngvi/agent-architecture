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
