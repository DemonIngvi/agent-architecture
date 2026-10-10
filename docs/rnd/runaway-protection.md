# R&D: защита от зацикливания и перерасхода

← [Все R&D](README.md) · компонент: Guardrails · решение: [design D6](../../openspec/changes/define-agent-platform/design.md) · спека: [guardrails](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md)

## Практики индустрии

| Практика | Где применяется | Что берём |
|---|---|---|
| Лимит итераций цикла | LangGraph `recursion_limit`, OpenAI Agents SDK `max_turns` | `limits.max_steps` |
| Детектор повторов одинаковых вызовов | агентные фреймворки, IDE-агенты | 3 одинаковых вызова подряд → стоп |
| Нет прогресса | ревью-циклы агентов | 8 шагов без изменения состояния → стоп |
| Бюджеты с мягким и жёстким порогом | LiteLLM budgets, облачные биллинги | 80% — предупреждение, 100% — отказ |
| Иерархия бюджетов | LiteLLM: ключ → команда → организация | вызов → запуск → агент/сутки → проект/месяц |
| RPM / TPM | лимиты провайдеров, LiteLLM | на модель и агента |
| Circuit breaker | надёжность распределённых систем | 3 ошибки подряд → стоп |
| Kill switch | эксплуатация | агент и платформа |

## Решение

Все проверки детерминированные (кодом, без LLM): G1 — бюджеты и kill switch до старта; G2 — шаги, повторы, прогресс, аномалии, ошибки; G4 — бюджеты и RPM/TPM на каждый вызов.

## Источники

- [LangGraph](https://github.com/langchain-ai/langgraph) · [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [LiteLLM: бюджеты и лимиты](https://docs.litellm.ai/)
- Проект AI-агент: `runtime/token-limits.md`
