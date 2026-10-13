# Замечания: LLM Gateway

← [компонент](../../../components/llm-gateway/index.md) · [подтверждения документов](../../approvals-summary.md) · [правило](../../rules/review-methodology.md#findings)

## Проверка ролями (пачка, 13.10.2026)

Пакетная проверка по карточкам (агент doc-batch-reviewer, Sonnet): все роли страниц компонента за проход; механику до ролей закрыл lint.

| № | Документ | Роли | Отклонение | Как закрыть | Где | Методология | Статус |
|---|---|---|---|---|---|---|---|
| Z-LLM-1 | components/llm-gateway/index.md | Р | У POST /v1/chat/completions и POST /key/generate ошибки: —, хотя блоки описывают отказы по алиасу (R-LLM-01), лимиту (R-LLM-05), run_id (R-LLM-03) → добавить коды ошибок в interfaces | правка | см. отклонение | нет — проверка ролью | ✅ коды ошибок добавлены в data/endpoints/llm-gateway.yaml: 401/400/429/5xx по R-LLM-01/03/05, key/generate: 401/400/404 |
| Z-LLM-2 | data-by-component/llm-gateway/index.md | Р | POST /v1/chat/completions и POST /key/generate с ошибки: — , но R-LLM-01/03/05 требуют отказ по алиасу, run_id и лимиту → указать коды (400/429) и тело ошибки | правка | см. отклонение | нет — проверка ролью | ✅ то же: коды и формат тела {error:{message,type,code}} в endpoints/llm-gateway.yaml |
| Z-LLM-3 | docs/api/llm-gateway.md | Р | Все четыре эндпоинта с ошибки: —, хотя R-LLM-01 (ошибка алиаса), R-LLM-03 (без run_id отклонён), R-LLM-05 (лимит) → задать коды и тело ошибок | правка | см. отклонение | нет — проверка ролью | ✅ то же: заполнено для chat/completions и key/generate; GET-эндпоинты правило не требует |
