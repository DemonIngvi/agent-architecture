Порядок работы компонента: что за чем происходит внутри и с соседями (источник — `docs/how/infrastructure.md`, на сайте — вкладка «Архитектура» компонента). Поля данных — в [Модели данных](../../data-model.md), стороны и протоколы — в «Интеграциях» компонента, сквозной сценарий — в [архитектуре](../../architecture.md#interaction).

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
