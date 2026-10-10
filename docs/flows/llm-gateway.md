# Потоки: LiteLLM gateway

← [Все потоки](README.md)

## Потоки

| # | Поток | От → к | Данные |
|---|---|---|---|
| 1 | Запрос к модели по алиасу | Harness → LiteLLM | `chat.completions`, virtual key агента |
| 2 | Проверка бюджета и rate limit | LiteLLM → LiteLLM | ключ, лимиты |
| 3 | Проверки G4 | LiteLLM хуки | вход и ответ |
| 4 | Маршрут к модели | LiteLLM → провайдер / mock | запрос провайдера |
| 5 | Резервная модель при сбое | LiteLLM → fallback | тот же запрос |
| 6 | Учёт затрат | LiteLLM → spend log → Observability | токены, $, `run_id` |

## Данные

Запрос Harness:

```http
POST /v1/chat/completions
Authorization: Bearer sk-agent-analyst
```

```json
{ "model": "team-default",
  "messages": [{ "role": "system", "content": "Ты аналитик…" }, { "role": "user", "content": "MKT-42: …" }],
  "tools": [{ "type": "function", "function": { "name": "add_comment", "parameters": { "type": "object" } } }],
  "metadata": { "run_id": "run_01J9Z4K", "issue_key": "MKT-42", "agent": "analyst" } }
```

Конфиг алиасов (mock для разработки):

```yaml
model_list:
  - model_name: team-default
    litellm_params: { model: openai/mock, api_base: http://mock-llm:8000/v1 }
  - model_name: team-default-fallback
    litellm_params: { model: anthropic/claude-sonnet-5 }
router_settings:
  fallbacks: [{ team-default: [team-default-fallback] }]
```

Сценарий mock-LLM (задача [1.1](../tasks/1.1-mock-llm-litellm.md)):

```yaml
- match: "MKT-42"
  steps:
    - tool_call: { name: add_comment, arguments: { issue: MKT-42, body: "Готово" } }
    - text: "Комментарий оставлен."
```
