# R&D: движок guardrails

← [Все R&D](README.md) · компонент: Guardrails · решение: [design D6](../../openspec/changes/define-agent-platform/design.md)

## Варианты

| Критерий | OPA (Rego) | Cedar | Проверки в коде |
|---|---|---|---|
| Лицензия | Apache 2.0, CNCF graduated | Apache 2.0 | — |
| Правила отдельно от кода | ✅ | ✅ | ❌ |
| Тесты политик | ✅ `opa test` | ✅ | юнит-тесты кода |
| Журнал решений (аудит) | ✅ встроен | ⚠️ свой | ❌ писать |
| Порог входа | язык Rego | проще | нет |
| Экосистема | широкая (k8s, API-шлюзы) | меньше | — |
| Риск | мейнтейнеры Styra ушли в Apple (2025), проект в CNCF | молодой | правила размазаны |

## Почему 4 точки

Одна проверка не закрывает все риски: G1 — до запуска (дёшево), G2 — смысл действия, G3 — ОС и сеть (не обойти), G4 — весь LLM-трафик. Каждая включается отдельно в конфиге деплоя.

## Решение

OPA для G1/G2: логика (Rego) в git, данные (allowlist, лимиты) в БД ICPlan; G3 — средства контейнера и сети; G4 — хуки LiteLLM.

## Источники

- [Open Policy Agent](https://www.openpolicyagent.org) · [GitHub (Apache-2.0)](https://github.com/open-policy-agent/opa)
- [Cedar](https://www.cedarpolicy.com)
- Проект AI-агент: решение 1.2 (OPA), `runtime/opa-placement.md`, `platform/technical/layers-and-mcp.md` §4
