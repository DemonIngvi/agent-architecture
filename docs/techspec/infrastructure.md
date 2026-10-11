# Техспека: Инфраструктура

← [Все техспеки](README.md) · [компонент](../../components/infrastructure/index.md) · [правило](../rules/tech-spec.md)

**Что разворачивается:** k3s на одном узле, Helm-чарты, Traefik, CloudNativePG + PgBouncer, RustFS, бэкапы вне площадки.

## Образы

| Образ | База | Что внутри | Как собирается | Откуда берём | Тег | Пользователь | Порты | Проверка готовности |
|---|---|---|---|---|---|---|---|---|
| k3s | установщик `get.k3s.io`, версия `v1.37.1+k3s1` | Kubernetes, Traefik, local-path | скрипт установки с закреплённой версией | github.com/k3s-io/k3s releases | v1.37.1+k3s1 | — | 6443 | `kubectl get --raw /readyz` |
| postgresql | `ghcr.io/cloudnative-pg/postgresql:17` (pgvector в комплекте) | Postgres 17 | оператор CloudNativePG | GHCR CloudNativePG, закреплён digest | 17.x | postgres | 5432 | проверки оператора |
| pgbouncer | Pooler CloudNativePG | PgBouncer transaction | ресурс `Pooler` | образ оператора | версия оператора | — | 5432 | проверки оператора |
| rustfs | `rustfs/rustfs:1.0.0` | S3-совместимое хранилище | официальный образ | Docker Hub, закреплён digest | 1.0.0 | non-root | 9000 | `/health` |

## Запуск

| | |
|---|---|
| **Порядок** | CNPG → Postgres → PgBouncer → RustFS → ICPlan → LiteLLM, OPA → Runner |
| **Бэкап** | WAL-архив и копии CNPG в внешнее S3 на другой площадке |
| **Секреты** | Secret кластера; ротация без простоя |

## Переменные и секреты

| Переменная | Зачем | Откуда |
|---|---|---|
| `values.yaml` | параметры L0 платформы | git платформы (без секретов) |

## Сборка и поставка

1. Чарты в git платформы, `helm lint` и `values.schema.json` в CI
2. Сборка в GitHub Actions по тегу `vX.Y.Z` репозитория компонента; базовые образы закреплены по digest
3. Многостадийный Dockerfile: стадия сборки → минимальный образ запуска без компиляторов и менеджеров пакетов
4. SBOM (`syft`) и проверка уязвимостей (`trivy`, блокирует выпуск при critical)
5. Публикация в `ghcr.io/demoningvi/<имя>:<версия>` и `:<версия>-<sha>`; тег `latest` не используется
6. Кластер тянет образы с pull-секретом `ghcr-pull` (Secret в namespace)

## Проверка после развёртывания

- [ ] `helm install` на чистом сервере проходит
- [ ] Восстановление БД из копии на тестовом узле


## Как работает {#how}

Порядок работы компонента: что за чем происходит внутри и с соседями. Поля данных — в [Модели данных](../../data-model.md), стороны и протоколы — в «Интеграциях» компонента, сквозной сценарий — в [архитектуре](../../architecture.md#interaction).

### Порядок работы


| # | Поток | От → к | Протокол | Данные |
|---|---|---|---|---|
| 1 | Вход пользователя | Браузер → Traefik → `web` / `api` | HTTPS (I21) | HTML / JSON |
| 2 | MCP агентов | Harness → Traefik или Service → `api /mcp` | HTTP (I9) | JSON-RPC |
| 3 | Запросы к БД | Сервисы → PgBouncer → PostgreSQL | протокол PostgreSQL (I22) | SQL |
| 4 | Вложения и артефакты | Runner / ICPlan → RustFS | S3 API (I19) | файлы |
| 5 | Резервные копии | CloudNativePG → S3 вне узла | S3 API | базовые копии + WAL |
| 6 | Создание запусков (этап 4) | Agent Runner → Kubernetes API | HTTPS (I23) | манифест Pod |
| 7 | Развёртывание | Администратор → Helm → Kubernetes API | HTTPS | чарты, values, Secret |

### Порядок запуска


```
PostgreSQL ─▶ PgBouncer ─▶ RustFS ─▶ api (миграции) ─▶ web, worker, bot
                                   └▶ LiteLLM, OPA, Memory API ─▶ Agent Runner ─▶ пул sandbox
```

## Пример конфигурации

Как настройки лежат в развёртывании. Значения и границы параметров — в `interfaces.md` спеки (здесь новых не вводится); поля контрактов — в [Модели данных](../../data-model.md).

Фрагмент `values-server.yaml`:

```yaml
ingress:
  host: plan.example.com
  tls: { acme: true }
api:      { replicas: 2, resources: { requests: { cpu: 300m, memory: 512Mi }, limits: { cpu: "1", memory: 1Gi } } }
litellm:  { replicas: 2, resources: { requests: { cpu: 300m, memory: 800Mi } } }
opa:      { replicas: 2, resources: { requests: { cpu: 50m, memory: 128Mi } } }
pgbouncer: { poolMode: transaction, defaultPoolSize: 30 }
postgres:
  backup: { target: s3://backup-offsite/itsaplan, schedule: "0 3 * * *" }
objectStorage: { endpoint: http://rustfs.itsaplan-data:9000, bucket: planner-attachments }
existingSecret: itsaplan-secrets
networkPolicy: { enabled: true }
```
