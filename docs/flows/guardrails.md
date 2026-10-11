# Потоки: Guardrails

← [Все потоки](README.md)

## Потоки

| # | Поток | Точка | От → к | Данные |
|---|---|---|---|---|
| 1 | Правила (логика) | — | git → OPA bundle | Rego |
| 2 | Данные правил | — | Platform module → OPA | allowlist, лимиты |
| 3 | Включение точек | — | конфиг деплоя → сервисы | `guardrails.gN.enabled` |
| 4 | Допуск запуска | G1 | Runner → OPA | `PolicyInput` → `PolicyDecision` |
| 5 | Проверка действия | G2 | Harness → OPA | `PolicyInput` → `PolicyDecision` |
| 6 | Изоляция | G3 | профиль → Sandbox | сеть, ФС, ресурсы |
| 7 | Проверка запроса к модели | G4 | LiteLLM хуки | PII, injection, модерация |
| 8 | Аудит | все | точки → Observability | `RunEvent` (`CUSTOM` `guardrail_decision`) |

## Данные

`PolicyInput` для G2 и ответ OPA:

Поля — [`PolicyInput`](../../data-model.md#model-policyinput) · [`PolicyDecision`](../../data-model.md#model-policydecision); пример — [каталог API](../api/README.md#policyinput-policydecision). Здесь копия не ведётся: модели и примеры живут в одном источнике ([правило](../rules/change-process.md#single-source)).

Правило (Rego, в git):

```rego
package agent.g2
default allow := false
allow if input.tool in data.agents[input.agent].tools_allow
confirm if input.tool in data.agents[input.agent].approval
```

Конфиг деплоя:

```yaml
guardrails:
  engine: opa
  g1: { enabled: true,  on_engine_error: deny }
  g2: { enabled: true,  on_engine_error: deny, approval: true }
  g3: { enabled: true }
  g4: { enabled: false }
```
