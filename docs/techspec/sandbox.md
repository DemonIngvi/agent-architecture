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
