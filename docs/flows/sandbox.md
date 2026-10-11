# Потоки: Sandbox

← [Все потоки](README.md)

## Потоки

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

## Данные

`SandboxClaim`:

Поля — [`SandboxClaim`](../../data-model.md#model-sandboxclaim); пример — [каталог API](../api/README.md#sandboxclaim). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).

`RepoGrant` — доступ к репозиторию на один запуск:

Поля — [`RepoGrant`](../../data-model.md#model-repogrant); пример — [каталог API](../api/README.md#repogrant). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).

Профиль sandbox:

```yaml
profile: light
image: harness:0.3.1
resources: { cpu: 1, memory_mb: 1024, disk_mb: 2048 }
network:
  egress_allow: [litellm, api, memory, opa, github.com]
pool: { size: 2 }
```
