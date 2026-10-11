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

<!-- flow-data -->
