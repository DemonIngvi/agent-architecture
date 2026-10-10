# User Stories: Harness

← [Все истории](README.md) · [потоки](../flows/harness.md)

> Сгенерировано из `html-view/stories.py` — правьте там.

## Процесс (BPMN)

<!-- bpmn:harness -->

| Шаг | Дорожка | Тип | Переходы | Артефакты |
|---|---|---|---|---|
| RunBundle | Harness | начало | → Собрать контекст | — |
| Собрать контекст | Harness | задача | → Вызов модели | контекст (M0) |
| Вызов модели | LiteLLM / MCP / OPA | задача | → Тулы? | chat.completions, spend log |
| Тулы? | Harness | развилка | да → G2 решение; нет → Quality gate? | — |
| G2 решение | LiteLLM / MCP / OPA | развилка | allow → Вызов тула; confirm → Подтверждение; deny → Собрать контекст | PolicyDecision |
| Подтверждение | Пользователь | задача | да → Вызов тула; нет → Собрать контекст | ApprovalDecision |
| Вызов тула | LiteLLM / MCP / OPA | задача | → Собрать контекст | результат тула |
| Quality gate? | Harness | развилка | пройден → RunResult; не пройден → gate_failed | — |
| gate_failed | Harness | ошибка | — | отчёт gate |
| RunResult | Harness | конец | — | RunResult |

## Истории

### US-HAR-01

**Как** агент-исполнитель ([персона Аг](personas.md#аг-агент-исполнитель)), **я хочу** выполнить задачу по инструкции, используя модель и тулы, **чтобы** получить результат.

**Критерии приёмки:**

- [ ] Ответ без тулов → завершение
- [ ] Вызов тула → результат в следующий шаг
- [ ] Битое определение → `invalid_definition`

**Требования:** [Инициализация из определения агента](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) · [Агентский цикл](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md)

### US-HAR-02

**Как** пользователь icplan ([персона П](personas.md#п-пользователь-icplan)), **я хочу** подтвердить опасное действие агента, **чтобы** агент не делал необратимое без меня.

**Критерии приёмки:**

- [ ] Пауза → запрос в задаче
- [ ] Одобрено → продолжение с того же шага
- [ ] Отклонено / таймаут → без действия

**Требования:** [Пауза и возобновление](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) · [G2 Action](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md)

### US-HAR-03

**Как** пользователь icplan ([персона П](personas.md#п-пользователь-icplan)), **я хочу** получить проверенный результат, **чтобы** не разбирать брак вручную.

**Критерии приёмки:**

- [ ] Gate пройден → `succeeded`
- [ ] Gate не пройден → повтор, затем `gate_failed` с причинами
- [ ] Критериев нет → отметка «gate не задан»

**Требования:** [Quality gate результата](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md)

### US-HAR-04

**Как** эксплуатация (devops) ([персона Э](personas.md#э-эксплуатация-devops)), **я хочу** чтобы агент не зацикливался и не тратил лишнее, **чтобы** траты были предсказуемыми.

**Критерии приёмки:**

- [ ] Повтор одинакового вызова 3 раза → стоп
- [ ] Лимит шагов → `limit` с частичным итогом
- [ ] Ошибки подряд → circuit breaker

**Требования:** [Завершение](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) · [Защита от зацикливания](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md) · [Circuit breaker на ошибки](../../openspec/changes/define-agent-platform/specs/guardrails/spec.md)

### US-HAR-05

**Как** эксплуатация (devops) ([персона Э](personas.md#э-эксплуатация-devops)), **я хочу** чтобы падение процесса не теряло работу, **чтобы** долгие задачи доходили до конца.

**Критерии приёмки:**

- [ ] Падение → продолжение с checkpoint
- [ ] Checkpointer недоступен → опасные действия отклоняются

**Требования:** [Пауза и возобновление](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md) · [Поведение при отказах зависимостей](../../openspec/changes/define-agent-platform/specs/agent-harness/spec.md)

