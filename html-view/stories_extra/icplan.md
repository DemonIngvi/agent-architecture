## Процесс задачи {#process}


Однозначная модель: **тип задачи = тип процесса**, **шаг процесса = колонка + агент + переходы**, **переход делает ICPlan по итогу запуска**. Спека: [icplan-agent-autopickup](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md) (R-AP-01, R-AP-02, R-AP-15…R-AP-17).

```
 Тип задачи «Исследование»                 Тип задачи «Фича»
 ┌──────────────┐  успех: процесс «Фича»   ┌──────────────┐ успех ┌──────────────┐ успех ┌──────────────┐ успех
 │ R&D          │─────────────────────────▶│ SDD          │──────▶│ Код          │──────▶│ Ревью        │──────▶ завершить
 │ агент: Ресёрч│   (тип меняется,          │ агент: Анал. │       │ агент: Разр. │       │ человек      │
 └──────┬───────┘    первый шаг «Фичи»)     └──────┬───────┘       └──────┬───────┘       └──────────────┘
        │ ошибка                                   │ ошибка               │ ошибка / лимит 3
        ▼                                          ▼                      ▼
   «Нужна помощь» (ручной шаг, владелец процесса, уведомление)

 Очередь агента «Разработчик»: все запуски, где он агент шага, по всем процессам → порядок: приоритет задачи, время постановки
```

### Термины

- **Процесс** — маршрут задачи одного типа: упорядоченные шаги, первый шаг, владелец.
- **Шаг** — колонка проекта + агент (или пусто — ручной шаг) + переход при успехе + переход при ошибке + лимит запусков.
- **Итог запуска** — успех, ошибка (в том числе лимит и непройденный quality gate), ждёт ответа, отменено человеком.
- **Очередь агента** — запуски, ждущие агента; выдаются по приоритету задачи, затем по времени.
- **Владелец процесса** — человек, которому уходит задача при ошибке шага.

Где это хранится — вкладка [«Данные»](../../data-by-component/icplan/index.md).

### Что пользователь видит при переходах

Правила переходов — в требованиях спеки; здесь — что появляется в истории задачи.

| Событие | Запись в истории задачи | Правило |
|---|---|---|
| Задача создана с типом, у которого есть процесс | «процесс X, шаг Y» | [R-AP-02 «Тип задачи задаёт процесс»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-02) |
| Задача вошла в шаг с агентом | «агент взял задачу: шаг Y» | [R-AP-01 «Агент шага процесса»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-01), [R-AP-05 «Защита от дублей»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-05), [R-AP-07 «Видимость подхвата»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-07) |
| Итог: успех | «итог: успех → шаг Z» | [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| Итог: ошибка или лимит запусков | «итог: ошибка (причина) → шаг E», «лимит шага» | [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| Итог: ждёт ответа | «ждёт ответа» | [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| Отменено пользователем | «отменено пользователем» | [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| Агент пытается сменить колонку | «агент: смена колонки отклонена» | [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16) |
| Смена типа задачи | «процесс X → процесс W» | [R-AP-02 «Тип задачи задаёт процесс»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-02) |

Чего процесс не делает (дочерние задачи вместо параллельных веток, агент не выбирает следующий шаг) — [R-AP-15 «Определение процесса»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-15), [R-AP-16 «Переход по итогу запуска»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-16).

Откуда у шага критерии приёмки и кто их подтверждает — [R-AP-15 «Определение процесса»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-15) (готовность шага), [R-AP-06 «Передача результата следующему этапу»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-06), [R-AP-18 «Проверка пользователем перед переходом»](../../openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/spec.md#r-ap-18); порядок при конфликте критериев — [design D20](../../openspec/changes/define-agent-platform/design.md).

## Как пользователь видит работу агента {#agent-feed}


Решение [D21](../../openspec/changes/define-agent-platform/design.md), разбор — [R&D «Вид работы агента в задаче»](../rnd/run-view.md). В карточке задачи — панель «Агент»: чат запуска на том же компоненте (`AgentChatPanel`) и протоколе AG-UI, что чат с агентом в форке.

```
 ┌ Задача MKT-42 · панель «Агент» ─────────────────────────────────────────┐
 │ ── Шаг «SDD» · агент analyst v5 · запуск #1042 · идёт 3 мин ─────────────│
 │ 🧭 План: ✓ прочитать задачу  ✓ собрать вводные  ▸ раздел «Требования»   │
 │ 💬 Читаю задачу и связанные документы, чтобы понять границы экспорта.   │
 │ ▸ 🔧 itsaplan_get_issue MKT-42 · 0,2 с                       [раскрыть] │
 │ ▸ 🧠 Рассуждение модели (сводка)                             [раскрыть] │
 │ ❓ Вопрос: нужна ли выгрузка в CSV?          [Ответить]                  │
 │ 👤 anna: да, CSV и XLSX                                                  │
 │ ⚠ Подтвердить: git_push в agent/MKT-42      [Одобрить] [Отклонить]       │
 │ ✅ Итог: spec.md готов · критерии 4/4 ✓ · 18 тыс. токенов · 0,12 $      │
 │    артефакты: spec.md, tasks.md · вердикт шага: [Принять] [Вернуть]     │
 │ ── Шаг «Код» · агент dev v3 · ждёт ───────────────────────────────────── │
 │ [ Написать агенту… ]                                          [Стоп]    │
 └─────────────────────────────────────────────────────────────────────────┘
```

| # | Поток | От → к | Данные |
|---|---|---|---|
| F1 | Агент действует: реплика о намерении, вызов тула, рассуждение модели (если есть) | Harness → Runner (I7) | `RunEvent` (`TEXT_MESSAGE_*`, `TOOL_CALL_*`, `REASONING_*`) |
| F2 | Маскирование и запись | Runner → ICPlan `POST /agent-runs/:runId/events` (I2) → S3 | дельты собраны в сообщение на `*_END` |
| F3 | Живая лента | ICPlan → браузер `GET /agent-runs/:runId/stream` (SSE) | события AG-UI по одному |
| F4 | История задачи по шагам | браузер → ICPlan `GET /issues/:issueId/agent-feed` | запуски, события, итоги |
| F5 | Вопрос или подтверждение | Harness → … → лента (`CUSTOM` `question` / `approval_request`) | карточка с кнопками |
| F6 | Ответ, подтверждение, указание, «стоп» | браузер → ICPlan → ответ heartbeat (I3) → Runner → Harness (I7) | `ApprovalDecision`, `UserMessage` |
| F7 | Итог и вердикт шага | Harness → Runner → ICPlan (`RunResult`); пользователь → `POST /issues/:issueId/agent-verdict` | карточка итога: критерии ✓ / ✗ (D20), артефакты, токены |

Что **не** показывается в ленте: промпты, полный вывод тулов без раскрытия, события `CUSTOM` `llm_call` — они у администратора в Observability.

У «Исследования» последний шаг — `"onSuccess": { "process": "Фича" }`: тип задачи меняется, задача встаёт на первый шаг «Фичи».
