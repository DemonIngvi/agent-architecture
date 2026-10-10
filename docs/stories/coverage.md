# Покрытие историй

← [Все истории](README.md) · [методика](../rules/us-methodology.md) · [персоны](personas.md)

> Сгенерировано при сборке из `html-view/stories.py`.

## Персона × компонент

Число историй; «·» — проверить, нет ли у персоны цели в этом компоненте ([методика, шаг 1](../rules/us-methodology.md)).

| Персона | ICPlan | Platform module | Agent Runner | Sandbox | Harness | Memory | MCP / Tools | Guardrails | LiteLLM gateway | Observability | Инфраструктура | Всего |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Пользователь ICPlan (П) | 4 | · | · | 1 | 2 | · | · | · | 1 | 1 | 1 | **10** |
| Администратор платформы (А) | 1 | 5 | · | 2 | · | 2 | 2 | 2 | 1 | 1 | · | **16** |
| Эксплуатация (DevOps) (Э) | 1 | · | 4 | 1 | 2 | · | · | 2 | 2 | 1 | 4 | **17** |
| Агент-исполнитель (Аг) | 1 | · | 1 | 2 | 1 | 2 | 1 | · | · | · | · | **8** |
| Владелец продукта (ВП) | · | · | · | · | · | · | · | · | · | · | · | **0** |
| Безопасность (Б) | · | · | · | · | · | · | · | · | · | · | · | **0** |
| Тестировщик / QA (QA) | · | · | · | · | · | · | · | · | · | · | · | **0** |
| Агент-ревьюер (АгР) | · | · | · | 1 | · | · | · | · | · | · | · | **1** |

## Истории с менее чем 3 критериями приёмки (30)

Нет альтернативных потоков или исключений ([шаг 4](../rules/us-methodology.md)).

- [US-ICP-06](icplan.md) — 2
- [US-PM-02](platform-module.md) — 2
- [US-PM-04](platform-module.md) — 2
- [US-PM-05](platform-module.md) — 2
- [US-RUN-02](agent-runner.md) — 2
- [US-RUN-03](agent-runner.md) — 2
- [US-RUN-05](agent-runner.md) — 2
- [US-SBX-03](sandbox.md) — 2
- [US-SBX-04](sandbox.md) — 2
- [US-SBX-07](sandbox.md) — 2
- [US-HAR-05](harness.md) — 2
- [US-MEM-02](memory.md) — 2
- [US-MEM-03](memory.md) — 2
- [US-MEM-04](memory.md) — 2
- [US-MCP-01](mcp-tools.md) — 2
- [US-MCP-02](mcp-tools.md) — 2
- [US-MCP-03](mcp-tools.md) — 2
- [US-GRD-01](guardrails.md) — 2
- [US-GRD-02](guardrails.md) — 1
- [US-GRD-03](guardrails.md) — 2
- [US-GRD-04](guardrails.md) — 2
- [US-LLM-01](llm-gateway.md) — 2
- [US-LLM-02](llm-gateway.md) — 2
- [US-LLM-03](llm-gateway.md) — 2
- [US-LLM-04](llm-gateway.md) — 2
- [US-OBS-01](observability.md) — 2
- [US-OBS-02](observability.md) — 1
- [US-OBS-03](observability.md) — 2
- [US-INF-02](infrastructure.md) — 2
- [US-INF-05](infrastructure.md) — 2

## Истории без требований (3)

- [US-SBX-05](sandbox.md)
- [US-SBX-06](sandbox.md)
- [US-SBX-07](sandbox.md)

Всего историй: **52**, персон: **8**, компонентов с историями: **11**.
