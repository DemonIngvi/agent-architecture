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

<!-- flow-data -->
