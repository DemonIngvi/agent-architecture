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

<!-- flow-data -->
