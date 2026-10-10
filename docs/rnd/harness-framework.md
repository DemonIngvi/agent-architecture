# R&D: фреймворк агентского цикла

← [Все R&D](README.md) · компонент: Harness · решение: [design D2](../../openspec/changes/define-agent-platform/design.md)

## Варианты

| Критерий | LangGraph | Свой цикл (проект AI-агент) | Claude Agent SDK | OpenAI Agents SDK |
|---|---|---|---|---|
| Лицензия | MIT | — | MIT | MIT |
| Пауза на approve (interrupt) | ✅ | ❌ писать | ⚠️ через hooks | ⚠️ |
| Восстановление после падения (checkpointer) | ✅ Postgres | ❌ писать | ❌ | ❌ |
| Стрим шагов | ✅ | ⚠️ писать | ✅ | ✅ |
| Любая модель через LiteLLM | ✅ OpenAI-совместимо | ✅ | ⚠️ формат Anthropic | ✅ |
| Hooks / middleware | ✅ узлы графа | как напишем | ✅ | ✅ guardrails |
| Риск | изменения API LangChain | объём своего кода | привязка к Anthropic | слабее паузы |

Довод проекта AI-агент «безопасность вне harness, значит цикл простой» верен для безопасности, но не покрывает approve, восстановление и таймлайн.

## Решение

LangGraph за своим интерфейсом harness; версия фиксируется.

## Источники

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- Проект AI-агент: `standard/harness.md` §6, решение 3.1
