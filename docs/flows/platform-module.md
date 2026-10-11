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

Поля — [`AgentSettings`](../../data-model.md#model-agentsettings); пример — [каталог API](../api/README.md#agentsettings). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).

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
