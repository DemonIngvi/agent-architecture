# Deploy: Guardrails

← [компонент](../../components/guardrails/index.md) · [методология](../rules/tech-spec.md)

**Что разворачивается:** OPA рядом с Runner и Harness; правила Rego из git; данные из Platform module.

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| opa | `openpolicyagent/opa:1.21.1-static` | OPA | официальный образ | Docker Hub, закреплён digest; копия в GHCR платформы | 1.21.1 | nonroot | 8181 | `GET /health?bundles` |
| opa-bundle | — | tar.gz: Rego из git + данные агентов | CI: `opa test` → `opa build`; данные — Platform module | объектное хранилище (S3) / HTTP Platform module | sha коммита правил | — | — | OPA сообщает версию бандла |

## Запуск

| | |
|---|---|
| **Реплики** | 2 |
| **Задержка** | на том же узле; p95 ≤ 20 мс; кэш решений `opa.cache_ttl_s` |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `OPA_BUNDLE_URL` | источник бандла | values |

## Сборка и поставка

1. Правила в git с тестами `opa test` (обязательно)
2. Сборка бандла в CI и публикация
3. Сборка в GitHub Actions по тегу `vX.Y.Z` репозитория компонента; базовые образы закреплены по digest
4. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
5. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
6. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`; тег `latest` не используется
7. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] Запрещённый тул → deny
- [ ] Без бандла → deny (`on_engine_error`)

## Пример конфигурации

Как настройки лежат в развёртывании. Значения и границы параметров — в `interfaces.md` спеки (здесь новых не вводится); поля контрактов — в [Модели данных](../../data-model.md).

Правило (Rego, в git):

```rego
package agent.g2
default allow := false
allow if input.tool in data.agents[input.agent].tools_allow
confirm if input.tool in data.agents[input.agent].approval
```

Конфиг деплоя:

```yaml
guardrails:
  engine: opa
  g1: { enabled: true,  on_engine_error: deny }
  g2: { enabled: true,  on_engine_error: deny, approval: true }
  g3: { enabled: true }
  g4: { enabled: false }
```
