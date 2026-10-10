# Потоки: Инфраструктура

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Протокол | Данные |
|---|---|---|---|---|
| 1 | Вход пользователя | Браузер → Traefik → `web` / `api` | HTTPS (I21) | HTML / JSON |
| 2 | MCP агентов | Harness → Traefik или Service → `api /mcp` | HTTP (I9) | JSON-RPC |
| 3 | Запросы к БД | Сервисы → PgBouncer → PostgreSQL | протокол PostgreSQL (I22) | SQL |
| 4 | Вложения и артефакты | Runner / ICPlan → RustFS | S3 API (I19) | файлы |
| 5 | Резервные копии | CloudNativePG → S3 вне узла | S3 API | базовые копии + WAL |
| 6 | Создание запусков (этап 4) | Agent Runner → Kubernetes API | HTTPS (I23) | манифест Pod |
| 7 | Развёртывание | Администратор → Helm → Kubernetes API | HTTPS | чарты, values, Secret |

## Порядок запуска

```
PostgreSQL ─▶ PgBouncer ─▶ RustFS ─▶ api (миграции) ─▶ web, worker, bot
                                   └▶ LiteLLM, OPA, Memory API ─▶ Agent Runner ─▶ пул sandbox
```

## Данные

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
