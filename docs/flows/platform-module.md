# Потоки: Platform module

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Администратор меняет настройки агента | Control Plane UI → API модуля | `AgentSettings` |
| 2 | Новая версия определения агента | API модуля → БД | `AgentDefinition` + версия |
| 3 | Runner читает профиль и бюджет перед запуском | Agent Runner → API модуля | `AgentSettings` |
| 4 | Алиасы и бюджеты уходят в LiteLLM | API модуля → LiteLLM | алиас, virtual key, лимит |
| 5 | Данные правил для OPA | API модуля → OPA (bundle data) | allowlist, лимиты |
| 6 | Экспорт / импорт агента | Админ ↔ API модуля | YAML `AgentDefinition` |

## Данные

`AgentSettings` — наши настройки агента, которых нет в ICPlan:

```json
{
  "agent_id": "ag_42",
  "model_alias": "team-default",
  "budget": { "daily_usd": 5, "per_run_tokens": 200000 },
  "sandbox_profile": "light",
  "memory_profile": "default",
  "guardrails": { "tools_allow": ["get_issue", "add_comment", "update_issue"], "approval": ["update_issue"] },
  "repos": [{ "repo": "org/app", "access": "write", "branch_prefix": "agent/" }]
}
```

`AgentDefinition` — формат экспорта/импорта (задача [1.2](../tasks/1.2-agent-definition-yaml.md)):

```yaml
apiVersion: agent/v1
id: analyst
version: 3
model: team-default
instructions: |
  Ты аналитик. По задаче пишешь требования в формате SDD.
skills: [sdd-writer]
mcp:
  - server: itsaplan-core
    tools: [get_issue, add_comment, update_issue]
limits: { max_steps: 30, timeout_s: 1800, max_tokens: 200000 }
approval: { tools: [update_issue] }
memory: { profile: default, read: [M2, M3, M6], write: [M3] }
sandbox: { profile: light }
```
