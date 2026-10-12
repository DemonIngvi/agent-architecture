# Замечания: Agent Runner

← [компонент](../../../components/agent-runner/index.md) · [подтверждения документов](../../approvals-summary.md) · [правило](../../rules/review-methodology.md#findings)

Проверка ролями 13.10.2026 (🤖, экономная: пакет review-pack, модель Sonnet; Архитектор, Разработчик, Тестировщик, DevOps, Сборка и поставка, Безопасность, Аналитик историй, Пользователь, Владелец продукта): 50 пар документ × роль — ✅ 29, ❌ 21. Страница компонента, данные, API, Deploy, истории, задачи 2.1 и 2.7 — без отказов. Пробелы lint (13) известны до проверки и в замечания не вошли.

| № | Документ | Роли | Отклонение | Как закрыть | Где | Методология | Статус |
|---|---|---|---|---|---|---|---|
| Z-RUN-1 | блоки admission, event-relay, finalizer, mcp-proksi, poller, run-supervisor, sandbox-claim, scheduler, shag-podgotovki, tokeny-repozitoriev | Р | карточка заполнена на 3–4 поля из 11: нет входов и выходов (тип данных, I-код), данных, параметров с именами из interfaces.md, задач | правка | `subcomponents.py`, карточки блоков Agent Runner | да → lint: неполная карточка блока (block-methodology.md#ready) | ⏳ |
| Z-RUN-2 | те же 10 блоков | Т | нет требований блока и «При сбое»: отказ G1 (admission), обрыв стрима (event-relay), ошибка записи итога или destroy (finalizer), отказ allowlist / G2 (mcp-proksi) и т. д. | правка | `subcomponents.py`: `reqs`, `failures` | да → lint (как Z-RUN-1) | ⏳ |
| Z-RUN-3 | components/agent-runner/sandbox-claim | А | не определено, кто владеет тёплым пулом и где он живёт; нет связи со слотами scheduler и SandboxProvider | правка | карточка sandbox-claim; источник `docs/rnd/sandbox-isolation.md` | нет — проверка ролью | ⏳ |
| Z-RUN-4 | docs/api/agent-runner.md | А | `/runs/:runId/deps` помечен I7, соседний `/runs/:runId/mcp/:server` — I9 (не блокирует) | проверить код интеграции | `datamodel.ENDPOINT_IO` | нет — проверка ролью | ⏳ |
| Z-RUN-5 | docs/tasks/2.1-runner-external.md | Р | в «Что проработать» открыт «Go или Python», хотя язык решён в D3 (не блокирует) | правка | задача 2.1 | нет — проверка ролью | ⏳ |
