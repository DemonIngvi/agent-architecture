# Техспека: Sandbox

← [Все техспеки](README.md) · [компонент](../../components/sandbox/index.md) · [правило](../rules/tech-spec.md)

**Что разворачивается:** одноразовый контейнер запуска на образе Harness; тёплый пул; сеть только через egress-прокси.

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| agent-harness (образ среды) | см. Harness | Harness + инструменты агента: git, ripgrep, python, node | см. Harness | `ghcr.io/demoningvi/agent-harness` | версия Harness | uid 10001, без sudo | 8090 (I7) | `GET /ready` Harness |
| egress-proxy | `ubuntu/squid:6` | Squid с allowlist доменов | конфиг из ConfigMap | Docker Hub `ubuntu/squid` (закреплён digest) | 6.x | squid | 3128 | TCP 3128 |

## Запуск

| | |
|---|---|
| **Изоляция** | read-only rootfs, `/workspace` — tmpfs / emptyDir по профилю, `no-new-privileges`, drop ALL capabilities, seccomp RuntimeDefault |
| **Сеть** | внутренняя сеть sandbox; выход только через `egress-proxy`; NetworkPolicy deny all, кроме прокси и Runner |
| **Профили** | `light` 1 CPU / 1 ГБ / 2 ГБ диска; `standard`, `heavy` — по таблице параметров |
| **Пул** | `pool.size` тёплых контейнеров на профиль |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `RUN_TOKEN` | одноразовый токен запуска (I7, I12) | Runner на запуск |
| `HTTPS_PROXY` | egress-прокси | Runner |
| токены git | не в env: подставляет прокси | — |
| ключи MCP-серверов | не в env и не в прокси: подставляет MCP-прокси Runner (D19) | — |
| секреты приватных реестров | только в контейнере подготовки (D19), в среду агента не передаются | Secret проекта |

Squid: две подсети источника — `sbx-agent` (только сервисы платформы и allowlist профиля) и `sbx-setup` (плюс `setup.registries`); правила `acl … src` + `dstdomain` (D19).

## Сборка и поставка

1. Образ среды = образ Harness
2. Squid: конфиг allowlist генерируется из политики доступа
3. Сборка в GitHub Actions по тегу `vX.Y.Z` репозитория компонента; базовые образы закреплены по digest
4. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
5. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
6. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`; тег `latest` не используется
7. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] Запрос к домену вне allowlist отклонён
- [ ] Контейнер удалён после запуска


## Как работает {#how}

Порядок работы компонента: что за чем происходит внутри и с соседями. Поля данных — в [Модели данных](../../data-model.md), стороны и протоколы — в «Интеграциях» компонента, сквозной сценарий — в [архитектуре](../../architecture.md#interaction).

### Порядок работы


| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Пул держит N готовых контейнеров на профиль | Sandbox → Docker | профиль |
| 2 | Runner забирает контейнер | Runner → пул | `SandboxClaim` |
| 3 | Клон разрешённых репозиториев в `/workspace` | контейнер → git | `RepoGrant` (через credential helper) |
| 4 | Весь исходящий трафик | контейнер → egress-прокси → allowlist | HTTP(S) |
| 5 | Подстановка секретов | egress-прокси → внешний API (к MCP — Runner, D19) | заголовки авторизации |
| 6 | Код наружу | контейнер → git | ветка `agent/<KEY>`, PR |
| 7 | Уничтожение и долив пула | Runner → пул | `sandboxId` |
| 8 | Шаг подготовки (D19): кэш по хешу lock-файлов или установка | Runner → контейнер подготовки (сеть `sbx-setup`) → Squid → `setup.registries` | `setup.script`, `/workspace/.deps` |
| 9 | Доустановка во время работы | Harness → тул `install_dependencies` → Runner → шаг подготовки | lock-файлы |
| 10 | Вызовы MCP | Harness → MCP-прокси Runner → MCP-серверы (из sandbox к MCP напрямую — нет) | `tools/list`, `tools/call` |

## Пример конфигурации

Как настройки лежат в развёртывании. Значения и границы параметров — в `interfaces.md` спеки (здесь новых не вводится); поля контрактов — в [Модели данных](../../data-model.md).

Профиль sandbox:

```yaml
profile: light
image: agent-harness:0.3.1
resources: { cpu: 1, memory_mb: 1024, disk_gb: 2 }
network:
  egress_allow: [litellm, api, memory, opa, github.com]
pool: { size: 2 }
```
