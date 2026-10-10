# Потоки: Sandbox

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Пул держит N готовых контейнеров на профиль | Sandbox → Docker | профиль |
| 2 | Runner забирает контейнер | Runner → пул | `SandboxClaim` |
| 3 | Клон разрешённых репозиториев в `/workspace` | контейнер → git | `RepoGrant` (через credential helper) |
| 4 | Весь исходящий трафик | контейнер → egress-прокси → allowlist | HTTP(S) |
| 5 | Подстановка секретов | egress-прокси → внешний API | заголовки авторизации |
| 6 | Код наружу | контейнер → git | ветка `agent/<KEY>`, PR |
| 7 | Уничтожение и долив пула | Runner → пул | `sandbox_id` |

## Данные

`SandboxClaim`:

```json
{ "profile": "light", "sandbox_id": "sbx-7f3a", "image": "harness:0.3.1", "cpu": 1, "memory_mb": 1024, "ready_ms": 140 }
```

`RepoGrant` — доступ к репозиторию на один запуск:

```json
{ "repo": "org/app", "access": "write", "branch_prefix": "agent/MKT-42", "protected": ["main"], "ttl_s": 3600 }
```

Профиль sandbox:

```yaml
profile: light
image: harness:0.3.1
resources: { cpu: 1, memory_mb: 1024, disk_mb: 2048 }
network:
  egress_allow: [litellm, api, memory, opa, github.com]
pool: { size: 2 }
```
