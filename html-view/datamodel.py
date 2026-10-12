"""Интеграции, контракты и модель данных компонентов — единый источник для карточек и страницы «Модель данных».

Источники:
- интерфейсы I1–I23 — матрица docs/data-types.md и таблицы «Интерфейсы обмена» в interfaces.md спек;
- эндпоинты — страницы каталога docs/api/*.md (сборка читает их сама);
- таблицы ICPlan — код форка, packages/db/src/schema/app.ts (icplan_schema.json + .meta.json с коммитом; обновлять: python html-view/schema_import.py [путь к форку], сборка сверяет коммит);
- таблицы платформы — проект схемы по спекам и решениям D4, D17–D20 (до реализации);
- таблицы LiteLLM — schema.prisma тега v1.104.2 (LITELLM_REF; колонки и типы сверены 2026-10-11).
Правило: docs/rules/change-process.md (новый интерфейс, хранилище или модель → этот файл).
"""

# ---------- интеграции ----------
# I-код → (от, к, через, что передаётся, модели). Слаги компонентов или внешние участники в «…».
INTEG = {
    "I1": ("agent-runner", "icplan", "", "Runner забирает запуск из очереди (`POST /agent-runs/claim`, pull, аренда 300 с); в ответе — `Run`", ["Run"]),
    "I2": ("agent-runner", "icplan", "", "шаги запуска и итог", ["RunEvent", "RunResult"]),
    "I3": ("agent-runner", "icplan", "", "Runner продлевает аренду (`POST /agent-runs/:runId/heartbeat`); сейчас ответ 204 без тела, отмена — ответом 404; после доработки (R-ICP-16) в ответе — отмена, решения по approve и указания пользователя", ["Heartbeat", "ApprovalDecision", "UserMessage"]),
    "I4": ("agent-runner", "platform-module", "", "настройки, определение версии запуска (`GET /platform/runs/:runId/agent`, D23), манифест", ["AgentSettings", "AgentDefinition", "WorkspaceSource"]),
    "I5": ("agent-runner", "guardrails", "", "допуск запуска G1", ["PolicyInput", "PolicyDecision"]),
    "I6": ("agent-runner", "sandbox", "", "Runner создаёт и уничтожает среду (Docker API) по `SandboxClaim`; `RepoGrant` задаёт правила git-прокси этой среды (какие репозитории и ветки), сам токен в среду не попадает", ["SandboxClaim", "RepoGrant"]),
    "I7": ("agent-runner", "harness", "", "Runner вызывает Harness: задание, подтверждения, указания и отмена → Harness; события и итог ← Harness", ["RunBundle", "UserMessage", "RunEvent", "ApprovalDecision", "RunResult"]),
    "I8": ("harness", "llm-gateway", "", "вызов модели", ["ChatCompletionRequest"]),
    "I9": ("harness", "mcp-tools", "agent-runner", "вызов тулов MCP через MCP-прокси Runner (D19)", ["McpToolCall"]),
    "I10": ("harness", "guardrails", "agent-runner", "проверка действия G2 (для MCP — повторно в Runner)", ["PolicyInput", "PolicyDecision"]),
    "I11": ("harness", "memory", "", "запись и чтение M3, контекст памяти", ["M3Record"]),
    "I12": ("harness", "agent-runner", "", "checkpoint цикла", ["Checkpoint"]),
    "I13": ("llm-gateway", "«провайдеры моделей / mock»", "", "запросы к моделям", ["ChatCompletionRequest"]),
    "I14": ("llm-gateway", "infrastructure", "", "ключи, бюджеты, журнал затрат в БД `litellm`", []),
    "I15": ("platform-module", "llm-gateway", "", "выдача virtual key, бюджеты", ["VirtualKey"]),
    "I16": ("platform-module", "guardrails", "", "бандл правил: данные из Platform module + Rego из git", ["OpaBundleData"]),
    "I17": ("sandbox", "«внешние хосты»", "", "исходящий трафик через egress-прокси (allowlist)", []),
    "I18": ("agent-runner", "«git-провайдер»", "", "короткоживущие токены репозиториев", ["RepoGrant"]),
    "I19": ("agent-runner", "infrastructure", "", "файлы задачи и артефакты в RustFS (S3 API)", []),
    "I20": ("icplan", "icplan", "", "интерфейс ICPlan ↔ API (в том числе экраны Platform module, чат запуска, сводка)", ["Process", "Verdict", "CostAggregate", "AgentDefinition", "AgentSettings"]),
    "I21": ("«пользователи»", "icplan", "infrastructure", "вход по HTTPS через Traefik: web, api, mcp", []),
    "I22": ("«сервисы»", "infrastructure", "", "Postgres через PgBouncer", []),
    "I24": ("agent-runner", "icplan", "", "MCP-прокси Runner вызывает MCP-сервер itsaplan-core в api ICPlan (`POST /mcp`) с ключом агента из Secret (D19); дальше I9 — к Harness", ["McpToolCall"]),
    "I23": ("agent-runner", "sandbox", "infrastructure", "среды запусков через Kubernetes API (этап 4)", ["SandboxClaim"]),
}
# Кто пользуется общими стыками I22 (БД) и I20 (API ICPlan), кроме владельцев
# Типы данных (Т1–Т8, docs/data-types.md) по интерфейсам
INTEG_TYPES = {
    "I1": "Т6, Т1 (задание)",
    "I2": "Т7, Т8 (итог), Т3 (ссылки на артефакты)",
    "I3": "Т6, Т1 (указания)",
    "I4": "Т4",
    "I5": "Т6, Т4",
    "I6": "Т4 (профиль среды), Т6",
    "I7": "Т6 (`RunBundle`), Т1, Т2, Т4, Т7, Т8",
    "I8": "Т1, Т2, Т8, Т7 (`metadata`), Т5 (virtual key)",
    "I9": "Т6 (вызов), Т8 (вывод), Т3",
    "I24": "Т6 (вызов), Т8 (вывод), Т3",
    "I10": "Т6, Т4",
    "I11": "Т2",
    "I12": "Т2 (состояние цикла)",
    "I13": "Т1, Т2, Т8, Т5 (ключ провайдера)",
    "I14": "Т7 (затраты), Т4 (ключи, бюджеты)",
    "I15": "Т4, Т5 (virtual keys)",
    "I16": "Т4 (правила, данные)",
    "I17": "Т3, Т5 (подстановка токена)",
    "I18": "Т5",
    "I19": "Т3",
    "I20": "Т1, Т3, Т4, Т7",
    "I21": "Т1, Т3, Т4",
    "I22": "Т1–Т7 (хранение)",
    "I23": "Т4 (манифесты), Т6",
}

# Интерфейсы, где стрелка (кто вызывает) обратна потоку данных: данные приходят в ответе вызываемого
DATA_IN_RESPONSE = {"I1", "I3", "I4"}

ALSO = {"I22": ["icplan", "platform-module", "agent-runner", "memory", "observability", "llm-gateway"],
        "I20": ["platform-module", "observability"], "I2": ["observability", "memory"], "I14": ["observability"],
        "I19": ["sandbox", "icplan"], "I17": ["sandbox", "mcp-tools"],
        "I8": ["guardrails"], "I7": ["sandbox"], "I18": ["sandbox"],
        "I4": ["icplan"]}  # I4 — Platform module встроен в api ICPlan (HOST): виден на C1 ICPlan

# ---------- модели обмена ----------
# имя → (назначение, [(поле, тип, обязательное, описание)])
MODELS = {
    "Run": ("запуск, выданный раннеру (`POST /agent-runs/claim` → `run`)", [
        ("id", "int", True, "`agent_run.id`"),
        ("trigger", "enum: mention · delegation · field · schedule · manual · process_step", True, "что создало запуск: упоминание агента в комментарии, назначение делегатом, изменение поля задачи, расписание, ручной запуск; `process_step` — шаг процесса (D17)"),
        ("prompt", "string", True, "задание, собранное ICPlan"), ("systemPrompt", "string", True, "правила самого запуска от ICPlan"),
        ("attempts", "int", True, "сколько раз запуск уже выдавался: аренда `AGENT_RUN_LEASE_SECONDS` = 300 с, Runner продлевает её heartbeat-ом (I3); не продлил — запуск выдаётся снова; после `AGENT_RUN_MAX_ATTEMPTS` = 3 выдач без итога следующий claim завершает его `failed` с `lastError` «Runner did not report a result» (`expireExhaustedRuns` форка)"),
        ("issueId", "int | null", True, "задача; `null` — запуск без задачи (расписание)"), ("issueIdentifier", "string | null", True, "читаемый ключ задачи, `MKT-42`"),
        ("rule", "{process, stepId}", False, "шаг процесса, создавший запуск, при `trigger = process_step` (D17): `process` — название типа задачи (= процесса), `stepId` — `ProcessStep.id`; иначе поля нет")]),
    "AgentDefinition": ("определение агента в YAML `agent/v1` — экспорт и импорт (R-REG-04, R-CP-05)", [
        ("apiVersion", "const: agent/v1", True, "версия формата"), ("id", "string", True, "имя агента (`username` в ICPlan)"),
        ("version", "int", True, "версия определения"), ("model", "string", True, "алиас LiteLLM"),
        ("instructions", "string", True, "инструкция агента"), ("skills", "string[]", False, "навыки"),
        ("mcp", "{server, tools[]}[]", False, "MCP-серверы и разрешённые тулы; источник — `project_resource` (`mcp`) и `access_policy` Platform module: MCP-серверов агента в форке нет (D23)"),
        ("limits", "{max_steps, timeout_s, max_tokens}", False, "параметры `limits.*`"), ("approval", "{tools[]}", False, "тулы с подтверждением"),
        ("memory", "{profile, read[], write[]}", False, "профиль памяти"), ("sandbox", "{profile}", False, "профиль среды")]),
    "RunSummary": ("итог прошлого запуска для памяти M2 — строка `agent_run` форка", [
        ("id", "int", True, "`agent_run.id`, как в API аналитики ICPlan"), ("agentId", "int", True, "агент"), ("status", "enum: pending · success · failed · canceled", True, "`agent_run.status`"),
        ("output", "string | null", False, "итог; в контекст попадает в пределах окна модели (управление контекстом, R-HRN-07)"), ("lastError", "string | null", False, "причина неудачи (`agent_run.last_error`)"),
        ("inputTokens / outputTokens", "int | null", False, "токены запуска"), ("finishedAt", "timestamp | null", False, "время завершения")]),
    "Heartbeat": ("ответ на продление аренды (`POST /agent-runs/:runId/heartbeat`) — обратный канал к раннеру; отмены в теле нет: отменённый запуск не `pending`, heartbeat отвечает 404 (как в форке) — Runner останавливает Harness", [
        ("approvals", "ApprovalDecision[]", False, "решения, ещё не доставленные; ICPlan повторяет их в каждом ответе, пока в событиях запуска не придёт `CUSTOM` `decision_applied` с этим `seq`; Runner отбрасывает повтор по `runId` + `seq`"), ("messages", "UserMessage[]", False, "указания, ещё не доставленные; повторяются, пока не придёт `CUSTOM` `message_received` с этим `id` (в ленте — «получено агентом»); повтор отбрасывается по `id`")]),
    "RunBundle": ("задание Harness от Runner (`POST /run`)", [
        ("runId", "int", True, "= `Run.id`"), ("agent", "{agentId, model, version, instructions, skills[]}", True, "определение агента версии запуска: `agent_run.agent_version`, закреплённой при первом вызове I4 `GET /platform/runs/:runId/agent` (D23); повторная выдача получает ту же версию (`instructions` — как поле `ai_agent.instructions` ICPlan)"),
        ("prompt / systemPrompt", "string", True, "задание и системные правила из `Run` без изменений"), ("guidance", "string", False, "руководство проекта для агентов (`project_platform.guidance`, Platform module)"), ("params", "map<string, any>", True, "итоговые параметры после слияния уровней L0 (развёртывание) → L1 (проект) → L2 (агент) → L3 (запуск); ключи — имена параметров конфигурации (`model.temperature`, `limits.max_steps`)"),
        ("workspace", "WorkspaceSource[]", False, "манифест рабочего пространства (R-RUN-17)"),
        ("memory", "{m3: M3Record, m2: RunSummary[]}", False, "память на старте: M3 этой задачи; M2 — итоги последних запусков (параметр `m2_last_runs`, по умолчанию 3); во время работы Harness пишет M3 в Memory API (I11)"),
        ("task", "{issueId, issueIdentifier, stepId, criteria: Criterion[], returnNote}", False, "задача и шаг процесса; `criteria` — только `active`: готовность шага, критерии человека, принятые критерии предыдущего шага и ревьюера (D20); `returnNote` — `Verdict.note` последнего возврата"),
        ("mcp", "{server, url, tools[]}[]", False, "MCP через прокси Runner (D19)")]),
    "WorkspaceSource": ("источник рабочего пространства", [
        ("name", "string", True, "имя в `/workspace/<имя>`"), ("type", "enum: git · folder", True, "вид"),
        ("url / prefix", "string", True, "при `type = git` — `url` репозитория; при `folder` — `prefix` папки в объектном хранилище RustFS (S3)"), ("branch", "string", False, "ветка агента `agent/<задача>`"),
        ("right", "enum: read · write", True, "право по политике (D18): `read` — вся папка и ветка задачи; `write` — только своя подпапка шага и ветка агента")]),
    "Criterion": ("критерий приёмки (D20)", [
        ("text", "string", True, "проверяемая формулировка"), ("origin", "enum: process · user:<username> · agent:<username> · reviewer:<username>", True, "кто задал: процесс, человек, агент предыдущего шага, ревьюер при возврате; `<username>` — `username` пользователя или агента ICPlan; порядок при конфликте: user и reviewer > process > agent; противоречие двух людей — агент задаёт вопрос исполнителю задачи (D20)"),
        ("status", "enum: active · pending_approval", True, "`pending_approval` — критерий агента ждёт подтверждения человеком (по `criteriaApproval` шага); проверка gate берёт только `active`")]),
    "RunEvent": ("событие запуска: конверт платформы вокруг события AG-UI (D21). Runner читает поток у Harness (`GET /run/events`, NDJSON) и пересылает в ICPlan (`POST /agent-runs/:runId/events`)", [
        ("runId", "int", True, "= `agent_run.id`"), ("seq", "int", True, "порядковый номер от Harness; ключ идемпотентности и порядка; Runner своих событий не нумерует, кроме `RUN_ERROR` при сбое среды (`seq` = последний + 1)"),
        ("at", "timestamp", True, "время события в Harness, ISO 8601 UTC"),
        ("event", "AgUiEvent", True, "событие AG-UI как есть: `type` и поля протокола")]),
    "AgUiEvent": ("событие протокола AG-UI", [
        ("type", "enum: RUN_STARTED · RUN_FINISHED · RUN_ERROR · STEP_STARTED · STEP_FINISHED · TEXT_MESSAGE_START · TEXT_MESSAGE_CONTENT · TEXT_MESSAGE_END · REASONING_START · REASONING_MESSAGE_START · REASONING_MESSAGE_CONTENT · REASONING_MESSAGE_END · REASONING_END · TOOL_CALL_START · TOOL_CALL_ARGS · TOOL_CALL_END · TOOL_CALL_RESULT · ACTIVITY_SNAPSHOT · CUSTOM", True, "тип события по протоколу"),
        ("runId / threadId", "string", False, "у `RUN_*`: `runId` — запуск строкой (так требует AG-UI); `threadId` — `issueIdentifier`, у запуска без задачи — `run-<runId>`"), ("stepName", "string", False, "у `STEP_*`: шаг цикла"),
        ("messageId / role / delta", "string", False, "у `TEXT_MESSAGE_*`, `REASONING_MESSAGE_*`: сообщение, роль, фрагмент текста; в хранилище платформы `*_END` несёт собранный текст сообщения в `delta` (D21)"),
        ("toolCallId / toolCallName / parentMessageId / content", "string", False, "у `TOOL_CALL_*`: вызов тула, имя, сообщение-родитель, результат"),
        ("activityType / content", "string / object", False, "у `ACTIVITY_SNAPSHOT`: `plan` и план `{done[], next[]}` из M3"),
        ("name", "string", False, "у `CUSTOM` — наш подтип: `question`, `approval_request`, `decision_applied`, `message_received`, `guardrail_decision`, `memory_write`, `llm_call`"), ("value", "object", False, "у `CUSTOM` — наши данные: `question` → `{text}`; `approval_request` → `{tool, argsHash, reason}`; `decision_applied` → `{seq}`; `message_received` → `{id}`; `guardrail_decision` → `{point: g1 · g2 · g4, allow, approval, reason}`; `memory_write` → `{level, scope}`; `llm_call` → `{model, inputTokens, outputTokens, costUsd}`"),
        ("message / code", "string", False, "у `RUN_ERROR`: причина")]),
    "RunResult": ("итог запуска (`POST /agent-runs/:runId/result`)", [
        ("status", "enum: success · failed", True, "отмену фиксирует ICPlan сам, раннер её не сообщает"),
        ("output", "string | null", False, "итог для истории; ICPlan обрезает до 10 000 символов"), ("error", "string | null", False, "причина при `failed`; ICPlan обрезает до 500 символов"),
        ("usage", "{inputTokens, outputTokens, reasoningTokens, costUsd, iterations}", False, "расход; `reasoningTokens`, `costUsd`, `iterations` (итерации цикла) — добавляем (D18)"),
        ("reason", "enum: done · limit · gate_failed · error", False, "причина Harness (R-RUN-07): `done` → `status = success`; `limit`, `gate_failed`, `error` → `failed`"),
        ("artifacts", "{name, url}[]", False, "опубликованное для человека: файл в RustFS (`s3://…`), ветка или PR (D20); в M3 — рабочие ссылки `{path, ref}`"),
        ("gate", "{passed: bool, failed: Criterion[]}", False, "проверка по критериям (R-HRN-08, D20): не выполненные критерии"),
        ("criteriaNext", "Criterion[]", False, "критерии, предложенные следующему шагу (D20, D26): Runner берёт их из итога Harness; ICPlan при приёме итога создаёт пункты чек-листа задачи с `origin = agent:<username>` и `status` по `criteriaApproval` шага")]),
    "ApprovalDecision": ("решение пользователя по вопросу или подтверждению", [
        ("runId", "int", True, ""), ("seq", "int", True, "`seq` события `CUSTOM` `approval_request` или `question`"), ("decision", "enum: approve · reject · answer", True, "на `approval_request` — `approve` или `reject`; на `question` — `answer`"),
        ("scope", "enum: once · run", False, "только для `approve`: этот вызов или такие же вызовы до конца запуска (R-GRD-03)"), ("by", "string", True, "`username` того, кто решил"), ("comment", "string | null", False, "при `answer` — ответ на вопрос; иначе пояснение")]),
    "UserMessage": ("указание пользователя во время работы", [
        ("id", "string", True, "идентификатор сообщения ICPlan, ключ от повторной доставки"), ("text", "string", True, "текст указания"), ("by", "string", True, "`username` автора"), ("at", "timestamp", True, "когда написано")]),
    "Verdict": ("вердикт по результату шага (R-AP-19)", [
        ("issueId / stepId", "int / string", True, "задача и шаг, по которому вердикт"), ("runId", "int | null", False, "запуск, чей итог оценивается; нет — ручной шаг"), ("verdict", "enum: accepted · rejected", True, "`accepted` → переход `onSuccess` шага, `rejected` → `onFailure`"), ("note", "string", False, "заметка возврата; следующий запуск шага, на который вернули задачу, получает её в `RunBundle.task.returnNote`"), ("by", "string", True, "`username` того, кто вынес вердикт"),
        ("criteria", "Criterion[]", False, "критерии ревьюера при возврате (D20)")]),
    "Process": ("процесс типа задачи (D17)", [
        ("issueType", "string", True, "тип задачи"), ("owner", "string", True, "`username` владельца процесса"), ("firstStep", "string", True, "`id` первого шага"),
        ("steps", "ProcessStep[]", True, "шаги"), ("version", "int", True, "версия; растёт при каждом изменении; задача на шаге дорабатывает его по старой версии, следующий шаг берёт из новой")]),
    "ProcessStep": ("шаг процесса (D17, D20)", [
        ("id", "string", True, "ключ шага в процессе (`sdd`) — колонка `process_step.key`, уникальна в процессе"), ("column", "string", True, "название колонки проекта (`SDD`)"), ("agentId", "int", False, "агент шага; нет — ручной шаг"),
        ("onSuccess / onFailure", "{step} · {process} · {done: true}", True, "куда переходит задача: на шаг этого процесса по `id`, на первый шаг другого процесса (тип задачи меняется) или завершается"), ("maxRuns", "int", False, "сколько раз шаг может запускаться по одной задаче, 1–10, по умолчанию 3 (R-AP-16); превышен — `onFailure`"),
        ("requireReview", "bool", True, "итог шага проверяет человек (вердикт), прежде чем задача перейдёт дальше"), ("deliverable", "string", False, "что шаг сдаёт: артефакты и формат (D20)"),
        ("doneCriteria", "Criterion[]", False, "готовность шага (D20)"), ("criteriaApproval", "enum: auto · review · always", True, "как подтверждаются критерии, предложенные агентом (D20): `auto` — без подтверждения, но если у шага `requireReview` или у агента-автора автономия R0–R1, работает как `review`; `review` — подтверждает человек при проверке шага; `always` — подтверждает человек всегда, до запуска шага")]),
    "M3Record": ("состояние задачи и передача следующему шагу (R-MEM-04, D20)", [
        ("issueId", "int", True, "задача, = `issue.id`; ключ записи — (задача, область)"), ("scope", "enum: issue · agent · project · team", True, "кто видит запись (R-MEM-02): агенты этой задачи, этот агент в других задачах, проект, команда"), ("agentId", "int", True, "автор записи"),
        ("done", "string[]", True, "сделано"), ("next", "string[]", True, "дальше"), ("blockers", "string[]", False, "что мешает продолжить"),
        ("artifacts", "{path, ref}[]", False, "артефакты: путь и ветка@коммит"), ("questions", "string[]", False, "открытые вопросы"),
        ("criteriaNext", "Criterion[]", False, "критерии, предложенные следующему шагу"), ("version", "int", True, "версия записи для конкурентной записи")]),
    "PolicyInput": ("вход OPA (G1, G2)", [
        ("point", "enum: g1 · g2", True, "G1 — допуск запуска, G2 — проверка действия агента"), ("agentId", "int", True, "агент; по нему правило находит `data.agents[<agentId>]`"), ("run", "{id, issueId, stepId}", True, "запуск, задача (или `null`), шаг процесса (или `null`, если запуск не по процессу)"),
        ("tool / argsHash", "string", False, "для G2: тул и SHA-256 его аргументов"), ("spent", "{dayUsd, monthUsd}", False, "для G1: потрачено агентом за день и проектом за месяц (считает Runner по журналу LiteLLM); лимиты, автономию и тулы правило берёт из данных бандла")]),
    "PolicyDecision": ("решение OPA", [
        ("allow", "bool", True, "можно ли выполнить сразу; при `true` поле `approval` = `false`"), ("approval", "bool", True, "при `allow = false`: `true` — можно после подтверждения человеком (пауза), `false` — запрещено"), ("reason", "string", True, "причина для аудита и ленты")]),
    "AgentSettings": ("настройки агента из Platform module (I4)", [
        ("agentId", "int", True, "агент"), ("version", "int", True, "единая версия агента: растёт при любой правке определения или настроек (R-CP-04); та же в `AgentDefinition.version` и `RunBundle.agent.version`"), ("autonomy", "enum: R0–R5", True, "уровень автономии: R0 — каждое действие с подтверждением … R5 — без подтверждений"),
        ("budget", "{runUsd, dayUsd}", True, "лимиты агента в $: на запуск и на день"), ("sandboxProfile", "string", True, "имя профиля среды (`sandbox_profile.name`)"), ("memoryProfile", "string", True, "имя профиля памяти"),
        ("toolsAllow / approvalTools", "string[]", True, "разрешённые тулы и тулы с подтверждением; в бандл OPA уходят как `tools_allow` и `approval`"), ("scheduling", "{parallel, max}", False, "`parallel` — сколько запусков агента идёт одновременно; `max` — сколько запусков агента может ждать в очереди")]),
    "SandboxClaim": ("заявка Runner на среду запуска", [
        ("profile", "string", True, "имя профиля среды"), ("sandboxId", "string", False, "в ответе: идентификатор среды, назначает провайдер"), ("image", "string", True, "образ Harness из профиля"),
        ("runtime", "enum: runc · runsc", True, "runc — обычный контейнер; runsc — gVisor, изоляция ядра для недоверенного кода (R-SBX-05)"), ("cpu / memoryMb / diskGb", "number", True, "ядра, МБ памяти, ГБ диска из профиля"), ("readyMs", "int", False, "в ответе: время до готовности среды")]),
    "RepoGrant": ("доступ к репозиторию на один запуск", [
        ("repo", "string", True, "репозиторий `org/name`"), ("access", "enum: read · write", True, "право на репозиторий"), ("branchPrefix", "string", True, "в какие ветки можно писать: `agent/`"),
        ("protected", "string[]", True, "ветки без записи"), ("ttlSec", "int", True, "срок токена; сам токен в модель не входит — его подставляет прокси (R-SBX-04)")]),
    "Checkpoint": ("состояние цикла (I12)", [
        ("runId", "int", True, "запуск"), ("iteration", "int", True, "номер итерации цикла Harness; ключ идемпотентности — `runId` + `iteration`"), ("parentIteration", "int", False, "предыдущая итерация"),
        ("state", "string (base64)", True, "сериализованное состояние графа LangGraph")]),
    "ChatCompletionRequest": ("запрос к модели (OpenAI Chat Completions через LiteLLM)", [
        ("model", "string", True, "алиас из `model_list`"), ("messages", "{role, content}[]", True, "слои промпта (R-HRN-18)"), ("tools", "{type, function: {name, parameters}}[]", False, ""),
        ("tool_choice / parallel_tool_calls", "enum / bool", False, "Harness: `auto`, без параллельных вызовов"), ("temperature / max_tokens / reasoning_effort", "number / enum", False, "`model.*`; неподдерживаемое отбрасывает `drop_params`"),
        ("metadata", "{run_id, issue_key, agent}", True, "наши ключи для атрибуции затрат (R-LLM-03): `run_id` = `Run.id`, `issue_key` = `issueIdentifier`, `agent` = `username`"), ("stream", "bool", False, "")]),
    "McpToolCall": ("вызов тула MCP (JSON-RPC 2.0)", [
        ("jsonrpc / id", "string / int", True, "конверт JSON-RPC 2.0"), ("method", "enum: tools/list · tools/call", True, ""), ("params.name", "string", False, "в запросе: имя тула"), ("params.arguments", "object", False, "в запросе: аргументы"),
        ("result.content", "{type, text}[]", False, "в ответе: результат; MCP-прокси Runner обрезает до `max_result_kb`"), ("error", "{code, message}", False, "в ответе при ошибке (JSON-RPC 2.0)")]),
    "VirtualKey": ("ключ LiteLLM на агента (`/key/generate`)", [
        ("key_alias", "string", True, "`agent:<agentId>`"), ("models", "string[]", True, "разрешённые алиасы"), ("max_budget", "float", True, "бюджет $ за период = `AgentSettings.budget.dayUsd`"),
        ("budget_duration", "string", True, "всегда `1d`: бюджет ключа = дневной лимит агента; лимит на запуск проверяет G1"), ("rpm_limit / tpm_limit", "int", False, ""), ("metadata", "object", False, "наши ключи в стиле LiteLLM: `agent_id`")]),
    "CostAggregate": ("сводка затрат по задаче и агенту (экран «Затраты», R-OBS-05)", [
        ("issueId", "int", True, "задача: `run_id` из журнала LiteLLM → `agent_run.issue_id`"), ("agentId", "int", True, "агент: `agent_run.agent_id`"), ("runs", "int", True, "число запусков за всё время задачи; запуски без задачи — в сводке агента (задача 3.9)"),
        ("inputTokens / outputTokens", "int | null", True, "токены из журнала LiteLLM; `null` — журнал недоступен, «неизвестно» (R-OBS-05)"), ("costUsd", "float | null", True, "затраты; `null` — цена модели не задана или журнал недоступен, стоимость неизвестна (R-OBS-05)")]),
    "OpaBundleData": ("данные бандла OPA (`data.json`)", [
        ("agents.<id>.tools_allow", "string[]", True, "`<id>` — `agentId`"), ("agents.<id>.approval", "string[]", True, "тулы с паузой"),
        ("agents.<id>.autonomy", "enum: R0–R5", True, ""), ("agents.<id>.budget", "{run_usd, day_usd}", True, "лимиты $ = `AgentSettings.budget`"), ("projects.<id>.budget.month_usd", "number", False, "лимит проекта на месяц = `project_platform.budget_month_usd`"), ("platform.kill_switch", "bool", True, "аварийная остановка всех агентов")]),
}

# Откуда модель и почему она такая (О-45): вид источника, ссылка, сноска «почему так, почему такие имена».
# fork — подтверждено OpenAPI форка (операция, часть, путь в JSON); сборка сверяет поля, не найденные в форке поля — только из PLANNED.
# ext — внешняя спецификация (ссылка); ours — наш контракт, решение D-…
NAMING = ("Имена полей: JSON наших контрактов — camelCase, как в API ICPlan (OpenAPI 1.3.0: `issueId`, `systemPrompt`, `inputTokens`, `lastError`); "
          "задача — парой `issueId` (ключ БД) и `issueIdentifier` (`MKT-42`), как в форке; единица измерения — суффиксом (`readyMs`, `memoryMb`, `costUsd`, `ttlSec`, как `durationMs`, `delaySec` в ICPlan). "
          "Внешние протоколы — в их стиле без перевода: OpenAI и LiteLLM (`max_tokens`, `key_alias`), MCP (`jsonrpc`, `params.arguments`), AG-UI (`toolCallId`), OPA (`input`, `result`). Колонки БД — snake_case, как в схеме Drizzle форка (поле JSON `criteriaNext` ↔ колонка `criteria_next`). "
          "Параметры конфигурации L0–L3 (YAML) — snake_case с точками, единица — суффиксом `_s`, `_mb` (`limits.max_steps`, `timeout_s`, `guardrails.tools_allow`); данные, выгружаемые из конфигурации как есть (бандл OPA), сохраняют эти имена. "
          "Агент в JSON — `agentId` (int, `ai_agent.id`); человек и агент как автор — `username` (строка); `<username>` в `origin` и `by` — тот же `username`.")
MODEL_META = {
    "Run": ("fork", "POST /agent-runs/claim", "response.run",
            "Это ответ форка любому внешнему раннеру: так ICPlan уже выдаёт запуски. `prompt` и `systemPrompt` разделены, потому что раннер передаёт первое как задание, второе — как системные правила. Мы добавляем только `rule` — какой шаг процесса создал запуск (D17): по нему Runner берёт критерии шага, а лента задачи — разделитель шага."),
    "AgentDefinition": ("ours", "R-REG-04, R-CP-05, задача 1.2",
                        "Файл для ревью и переноса агента между окружениями: снимок `ai_agent` (ICPlan) и `AgentSettings` (Platform module), источник правды — они, файл только читается и импортируется. Агент в файле — `id` = `username`, потому что числовой `agentId` в другом окружении другой. Имена — как у параметров конфигурации: YAML snake_case (`limits.max_steps`, `memory.read` — уровни памяти M0–M6), единицы — суффиксом `_s`. Исключение — `apiVersion`: заголовок формата, как в манифестах Kubernetes."),
    "RunSummary": ("ours", "R-MEM-03, R-MEM-05",
                   "M2 (эпизодическая память: итоги прошлых запусков) не хранится отдельно: это строки `agent_run` форка: ICPlan пишет их сам при выдаче и завершении запуска (`POST …/result`). Модель наша, данные и имена — форка (`GET /projects/:projectKey/analytics/agent-runs`: `id`, `agentId`, `lastError`)."),
    "Heartbeat": ("ours", "D17, R-ICP-16",
                  "Сейчас heartbeat в форке отвечает 204 без тела, а на отменённый или завершённый запуск — 404. Ответ с телом — доработка: так раннер узнаёт об ответах и указаниях без отдельного канала (раннер ходит наружу сам, входящих соединений нет). Отмена остаётся одним способом — 404, как в форке: поля `canceled` в ответе нет."),
    "RunBundle": ("ours", "D18, D19, D20",
                  "Всё, что нужно Harness на один запуск, одним документом: Harness не ходит в ICPlan сам (нет учётных данных в sandbox). Группы `agent`, `task`, `memory`, `workspace`, `mcp` — по источнику данных, чтобы было видно, кто за что отвечает."),
    "WorkspaceSource": ("ours", "D18", "Рабочее пространство собирается из источников проекта; `right` — право агента на источник по политике, его проверяет Runner при монтировании."),
    "Criterion": ("ours", "D20", "Критерий хранится пунктом чек-листа задачи ICPlan (`issue_checklist_item`) с полями `origin` и `status`. Происхождение нужно, чтобы применить порядок «человек > процесс > агент» и показать, кто что задал."),
    "RunEvent": ("ours", "D21", "Конверт добавляет к событию AG-UI то, чего в протоколе нет: номер запуска, сквозной `seq` для порядка и идемпотентности и время в Harness. Поля события не меняем — их понимает чат форка; единственное отличие в хранилище: дельты сообщения собираются, и `*_END` несёт полный текст в `delta`."),
    "AgUiEvent": ("ext", "https://docs.ag-ui.com/concepts/events",
                  "Протокол AG-UI без изменений; тот же формат форк уже принимает в чате агента (`POST /agent-chats/:messageId/events`, OpenAPI 1.3.0). Имена и регистр типов — по протоколу."),
    "RunResult": ("fork", "POST /agent-runs/{runId}/result", "request",
                  "Тело, которое форк уже принимает от раннера: `status`, `output`, `error`, `usage` с `inputTokens` и `outputTokens`. Добавляем то, без чего не работают D18 и D20: причину Harness, артефакты, проверку по критериям, стоимость и токены размышлений."),
    "ApprovalDecision": ("ours", "D17, R-GRD-03", "Решение привязано к `seq` события-вопроса: так Harness понимает, на какой вопрос ответ, даже если их несколько. Доставляется в ответе heartbeat."),
    "UserMessage": ("ours", "D17, R-ICP-16", "Указание пользователя во время запуска; доставляется в ответе heartbeat и попадает в ленту задачи."),
    "Verdict": ("ours", "D20, R-AP-19", "Вердикт шага из карточки итога; при возврате ревьюер может добавить критерии с происхождением `reviewer:<кто>`."),
    "Process": ("ours", "D17", "Процесс задаётся на тип задачи: тип задачи = тип процесса. Шаги — колонка, агент и переходы; так ICPlan сам двигает задачу, агент колонку не меняет."),
    "ProcessStep": ("ours", "D17, D20", "Шаг = колонка + агент + переходы (D17) и контракт шага (D20): что сдать и как проверить."),
    "M3Record": ("ours", "R-MEM-04, D20", "M3 — память состояния задачи и передача между шагами: «сделано / дальше / блокеры» и ссылки на артефакты вместо содержимого. Harness пишет её в Memory API (отдельный сервис платформы) по токену запуска, а не в БД; Memory API хранит её в `memory_m3` по ключу (задача, область), `version` защищает от одновременной записи."),
    "PolicyInput": ("ours", "D6, R-GRD-01", "Содержимое наше: точка G1 или G2, агент, запуск, тул и потраченный бюджет; конверт `{input: …}` задаёт REST API OPA. Вместо аргументов тула — их хеш, чтобы в аудите не было данных. Лимиты сюда не передаются: правило берёт их из данных бандла по `agentId`."),
    "PolicyDecision": ("ours", "D6, R-GRD-03", "Ответ нашего правила Rego, OPA кладёт его в `{result: …}`. Три исхода: выполнить сразу (`allow`), после подтверждения (`approval`), запрещено."),
    "AgentSettings": ("ours", "D9, R-CP-04", "Наши настройки агента, которых нет в ICPlan; источник правды для автономии, бюджета, тулов и профилей. Включён ли агент — не здесь: источник правды один, `ai_agent.enabled` ICPlan (D17, R-ICP-17); аварийная остановка — `kill_switch` (`agent:<id>`). Из них собираются бандл OPA (`OpaBundleData`, имена конфигурации) и файл экспорта (`AgentDefinition`). Версия нужна для отката и для того, чтобы запуск видел настройки версии, закреплённой при первом вызове I4 (D23)."),
    "SandboxClaim": ("ours", "D1, R-SBX-05", "Заявка Runner провайдеру среды (Docker, позже Kubernetes): профиль, образ и ресурсы."),
    "RepoGrant": ("ours", "D18, R-SBX-04", "Короткоживущий доступ к репозиторию на запуск: только ветки с префиксом агента, защищённые ветки без записи."),
    "Checkpoint": ("ours", "D2, D18, R-HRN-05", "Состояние графа LangGraph между шагами; Harness пишет его через Runner, потому что в sandbox нет учётных данных БД."),
    "ChatCompletionRequest": ("ext", "https://platform.openai.com/docs/api-reference/chat/create",
                              "Стандартный запрос OpenAI Chat Completions, который LiteLLM принимает для любого провайдера. `metadata` — наши ключи для атрибуции затрат; их имена в стиле LiteLLM, потому что они попадают в его журнал затрат."),
    "McpToolCall": ("ext", "https://modelcontextprotocol.io/specification", "Вызов тула по протоколу MCP поверх JSON-RPC 2.0; имена — по спецификации."),
    "VirtualKey": ("ext", "https://docs.litellm.ai/docs/proxy/virtual_keys", "Ключ LiteLLM на агента: бюджет и модели ограничиваются шлюзом, а не кодом агента. Ключ хранится в Secret и подставляется egress-прокси, в среду запуска не попадает (Т5). Имена — API LiteLLM, включая наши ключи `metadata`."),
    "CostAggregate": ("ours", "R-OBS-05, R-LLM-03", "Сводка для экрана затрат: Observability читает журнал LiteLLM (I14) и группирует по `metadata.run_id` → `agent_run`; токены названы как в ICPlan (`inputTokens`, `outputTokens`). `RunResult.usage` — расход одного запуска, сводка — сумма по журналу."),
    "OpaBundleData": ("ours", "D6, R-GRD-01", "Данные, которые Platform module кладёт в бандл OPA рядом с правилами Rego: что разрешено агенту, где нужна пауза, бюджет и аварийный выключатель. Это выгрузка параметров конфигурации как есть, поэтому имена — как у параметров (`guardrails.tools_allow`, `kill_switch`): их и читают правила Rego."),
}

# Значок источника поля, если он отличается от значка модели (О-48): модель → {поле: значок и пояснение}
FIELD_SRC = {
    "RunSummary": {n: "✅ форк (`agent_run`)" for n in ("id", "agentId", "status", "output", "lastError", "inputTokens / outputTokens", "finishedAt")},
    "Criterion": {"text": "✅ форк (`issue_checklist_item.content`)", "origin": "🛠 D20", "status": "🛠 D20"},
    "AgUiEvent": {"name": "🧩 наше (подтип)", "value": "🧩 наше"},
    "ChatCompletionRequest": {"metadata": "🧩 наши ключи"},
    "VirtualKey": {"metadata": "🧩 наши ключи"},
    "RunEvent": {"event": "📘 AG-UI; `*_END` в хранилище — с собранным `delta` (D21)"},
}

# Поля моделей «fork», которых в форке ещё нет: поле → решение
PLANNED = {
    "Run": {"rule": "D17", "trigger": "D17 (значение `process_step`)"},
    "RunResult": {"usage": "D18 (`reasoningTokens`, `costUsd`, `iterations`)", "reason": "R-RUN-07", "artifacts": "D20", "gate": "D20", "criteriaNext": "D26"},
}

# ---------- хранилища ----------
# Таблицы ICPlan из кода форка: компонент → [(ключ в icplan_schema.json, пометка)]
ICPLAN_TABLES = {
    "icplan": [("project", ""), ("projectColumn", ""), ("issueType", ""), ("issue", "+ `review_with_me` (D17)"), ("issueChecklist", ""),
               ("issueChecklistItem", "+ `origin`, `status` (D20)"), ("issueActivity", ""), ("aiAgent", "+ `enabled` (D17)"), ("agentRun", ""),
               ("agentSchedule", ""), ("agentChatThread", ""), ("agentChatMessage", ""), ("projectAction", "+ ключ `delegateUserId` в `effect` (R-AP-03)"),
               ("projectDocument", ""), ("issueAttachment", ""),
               ("user", "Better Auth; у агента — бот-пользователь"), ("apikey", "ключ агента: Bearer для I1–I3; `reference_id` → `user.id`")],
    "mcp-tools": [("aiAgent", ""), ("agentTool", ""), ("agentToolLink", ""), ("agentSkill", ""), ("agentSkillLink", ""),
                  ("integrationCredential", ""), ("project", "`mcp_enabled`"), ("gitProviderConnection", ""), ("gitManagedRepository", "")],
    "memory": [("agentChatMessage", "M1"), ("agentRun", "M2"), ("issueActivity", "M1, M2"), ("projectDocument", "M6"), ("aiAgent", "M5")],
    "observability": [("agentRun", "итоги, токены"), ("issue", "")],
}

# Таблицы платформы (проект схемы): имя → (хранилище, владелец, [(колонка, тип, ключ, описание)])
PLATFORM_TABLES = {
    "process": ("S1", "icplan", [("id", "serial", "PK", ""), ("project_id", "int", "FK project", ""), ("issue_type_id", "int", "FK issue_type", "один процесс на тип"),
                                 ("owner_user_id", "text", "", "владелец"), ("first_step_id", "int", "FK process_step", ""), ("version", "int", "", "версия процесса")]),
    "process_step": ("S1", "icplan", [("id", "serial", "PK", ""), ("key", "text", "", "ключ шага в процессе (`sdd`) — `ProcessStep.id`"), ("process_id", "int", "FK process", ""), ("column_id", "int", "FK project_column", "колонка"),
                                      ("agent_id", "int", "FK ai_agent", "нет — ручной шаг"), ("on_success", "jsonb", "", "шаг / процесс / завершить"), ("on_failure", "jsonb", "", ""),
                                      ("max_runs", "int", "", "3"), ("require_review", "bool", "", ""), ("deliverable", "text", "", "результат шага (D20)"),
                                      ("done_criteria", "jsonb", "", "готовность шага (D20)"), ("criteria_approval", "text", "", "auto / review / always")]),
    "issue_process_state": ("S1", "icplan", [("issue_id", "int", "PK, FK issue", ""), ("process_id", "int", "FK process", ""), ("process_version", "int", "", "составной FK (`process_id`, `process_version`) → `process_version`, индекс по этой паре; версия процесса, с которой задача вошла в текущий шаг: шаг дорабатывается по снимку этой версии (R-AP-22)"), ("step_id", "int", "FK process_step", "текущий шаг"),
                                             ("runs_on_step", "int", "", "счётчик для `max_runs`"), ("state", "text", "", "running / waiting_review / paused / done"),
                                             ("last_verdict", "text", "", "accepted / rejected"), ("updated_at", "timestamptz", "", "")]),
    "agent_settings": ("S2", "platform-module", [("agent_id", "int", "PK, FK ai_agent", ""), ("version", "int", "", "текущая версия"), ("autonomy_level", "text", "", "R0–R5"),
                                                 ("budget_run_usd", "numeric", "", ""), ("budget_day_usd", "numeric", "", ""), ("sandbox_profile_id", "int", "FK sandbox_profile", ""),
                                                 ("memory_profile_id", "int", "FK memory_profile", ""), ("tools_allow", "jsonb", "", ""), ("approval_tools", "jsonb", "", ""),
                                                 ("scheduling", "jsonb", "", "parallel, max"), ("updated_by", "text", "", ""), ("updated_at", "timestamptz", "", "")]),
    "agent_settings_version": ("S2", "platform-module", [("agent_id", "int", "PK, FK agent_settings", ""), ("version", "int", "PK", ""), ("data", "jsonb", "", "снимок определения агента и настроек (D26)"), ("definition_hash", "text", "", "хеш определения ICPlan: при вызове I4 отличие от последней версии создаёт новую (D26)"),
                                                         ("created_by", "text", "", ""), ("created_at", "timestamptz", "", "")]),
    "sandbox_profile": ("S2", "platform-module", [("id", "serial", "PK", ""), ("name", "text", "", "light, coder…"), ("image", "text", "", ""), ("runtime", "text", "", "runc / runsc"),
                                                  ("cpu", "numeric", "", ""), ("memory_mb", "int", "", ""), ("disk_gb", "int", "", ""), ("egress_allow", "jsonb", "", ""), ("pool_size", "int", "", "")]),
    "memory_profile": ("S2", "platform-module", [("id", "serial", "PK", ""), ("name", "text", "", ""), ("read", "jsonb", "", "уровни"), ("write", "jsonb", "", ""),
                                                 ("m2_last_runs", "int", "", "3"), ("retention", "jsonb", "", ""), ("scope", "text", "", "задача…")]),
    "project_resource": ("S2", "platform-module", [("id", "serial", "PK", ""), ("project_id", "int", "FK project", ""), ("kind", "text", "", "git / folder / document / mcp"),
                                                   ("ref", "text", "", "адрес, префикс, id"), ("name", "text", "", "")]),
    "access_policy": ("S2", "platform-module", [("id", "serial", "PK", ""), ("project_id", "int", "FK project", ""), ("agent_id", "int", "FK ai_agent", ""),
                                                ("resource_id", "int", "FK project_resource", ""), ("right", "text", "", "read / write (D18)"), ("template_role", "text", "", "шаблон по роли агента")]),
    "project_platform": ("S2", "platform-module", [("project_id", "int", "PK, FK project", ""), ("guidance", "text", "", "руководство проекта"), ("budget_month_usd", "numeric", "", ""),
                                                   ("setup_script", "text", "", "шаг подготовки (D19)"), ("lock_files", "jsonb", "", "для кэша")]),
    "kill_switch": ("S2", "platform-module", [("scope", "text", "PK", "platform / agent:<id>"), ("enabled", "bool", "", ""), ("reason", "text", "", ""), ("by", "text", "", ""), ("at", "timestamptz", "", "")]),
    "scheduler_slot": ("S3", "agent-runner", [("slot_key", "text", "PK", "global:N / agent:<id> / model:<alias> / issue:<id>"), ("run_id", "int", "FK agent_run", ""),
                                              ("runner_id", "text", "", "экземпляр Runner"), ("lease_until", "timestamptz", "", "аренда слота"), ("acquired_at", "timestamptz", "", "")]),
    "run_event": ("S3", "observability", [("run_id", "int", "PK, FK agent_run", "целое, как `agent_run.id`"), ("seq", "int", "PK", ""), ("ts", "timestamptz", "", ""),
                                          ("type", "text", "", "`event.type` AG-UI, для отбора"), ("event", "jsonb", "", "событие AG-UI целиком, маскированное; дельты собраны в сообщение"), ("issue_id", "int", "FK issue", "лента задачи")]),
    "setup_cache": ("S3", "agent-runner", [("lock_hash", "text", "PK", "хеш lock-файлов"), ("project_id", "int", "FK project", ""), ("path", "text", "", "том кэша"),
                                           ("created_at", "timestamptz", "", ""), ("expires_at", "timestamptz", "", "`setup.cache_ttl_h`")]),
    "memory_m3": ("S4", "memory", [("issue_id", "int", "PK, FK issue", ""), ("scope", "text", "PK", ""), ("agent", "text", "", "автор"), ("done", "jsonb", "", ""), ("next", "jsonb", "", ""),
                                   ("blockers", "jsonb", "", ""), ("artifacts", "jsonb", "", "D20"), ("questions", "jsonb", "", "D20"), ("criteria_next", "jsonb", "", "D20"),
                                   ("version", "int", "", ""), ("updated_at", "timestamptz", "", "")]),
    "m4_fact": ("S4", "memory", [("id", "bigserial", "PK", "после MVP"), ("scope", "text", "", ""), ("text", "text", "", "маскированный"), ("embedding", "vector", "", "pgvector"),
                                 ("source", "text", "", ""), ("valid_from", "timestamptz", "", ""), ("valid_to", "timestamptz", "", ""), ("superseded_by", "bigint", "FK m4_fact", "")]),
    "agent_run_delivery": ("S1", "icplan", [("id", "serial", "PK", ""), ("run_id", "int", "FK agent_run", "запуск"),
                           ("kind", "text", "", "approval · message"), ("seq", "int", "", "событие запроса подтверждения (для approval)"),
                           ("payload", "jsonb", "", "`ApprovalDecision` или `UserMessage`"), ("created_at", "timestamptz", "", ""),
                           ("delivered_at", "timestamptz", "", "Runner подтвердил получение: `decision_applied` · `message_received` (R-ICP-16)")]),
    "process_version": ("S1", "icplan", [("process_id", "int", "PK, FK process", ""), ("version", "int", "PK", "версия процесса"),
                        ("steps", "jsonb", "", "снимок шагов: задача дорабатывает шаг по версии, с которой вошла (R-AP-22)"), ("created_at", "timestamptz", "", "")]),
    "run_checkpoint": ("S5", "agent-runner", [("run_id", "int", "PK, FK agent_run", ""), ("iteration", "int", "PK", "итерация цикла"), ("parent_iteration", "int", "", ""), ("state", "bytea", "", "состояние LangGraph"),
                                              ("created_at", "timestamptz", "", ""), ("expires_at", "timestamptz", "", "`checkpoint.ttl`")]),
}
LITELLM_REF = "schema.prisma LiteLLM v1.104.2 (тег, fc3920bf)"
LITELLM_TABLES = {
    "LiteLLM_VerificationToken": [("token", "String", "PK", "virtual key (хеш)"), ("key_alias", "String", "", "`agent:<id>`"), ("models", "String[]", "", ""), ("spend", "Float", "", ""),
                                  ("max_budget", "Float", "", ""), ("budget_duration", "String", "", ""), ("rpm_limit", "BigInt", "", ""), ("tpm_limit", "BigInt", "", ""),
                                  ("budget_id", "String", "FK LiteLLM_BudgetTable", ""), ("team_id", "String", "", ""), ("metadata", "Json", "", ""), ("expires", "DateTime", "", "")],
    "LiteLLM_SpendLogs": [("request_id", "String", "PK", ""), ("api_key", "String", "", "virtual key"), ("model", "String", "", ""), ("spend", "Float", "", "$"),
                          ("prompt_tokens", "Int", "", ""), ("completion_tokens", "Int", "", ""), ("total_tokens", "Int", "", ""), ("startTime", "DateTime", "", ""),
                          ("endTime", "DateTime", "", ""), ("metadata", "Json", "", "run_id, issue_key, agent"), ("status", "String", "", "")],
    "LiteLLM_BudgetTable": [("budget_id", "String", "PK", ""), ("max_budget", "Float", "", ""), ("soft_budget", "Float", "", ""), ("budget_duration", "String", "", ""),
                            ("rpm_limit", "BigInt", "", ""), ("tpm_limit", "BigInt", "", "")],
    "LiteLLM_ProxyModelTable": [("model_id", "String", "PK", ""), ("model_name", "String", "", "алиас"), ("litellm_params", "Json", "", "провайдер, модель")],
}
# Хранилища компонента для страницы: слаг → [(хранилище, подпись)]
# Домены S1 на странице «Модель данных» — чтобы диаграмма читалась (О-44)
S1_DOMAINS = [
    ("Задачи и процесс", ["project", "project_column", "issue_type", "issue", "issue_checklist", "issue_checklist_item",
                          "project_action", "process", "process_step", "issue_process_state"]),
    ("Агенты, запуски, доступ", ["ai_agent", "agent_run", "agent_schedule", "agent_chat_thread", "agent_chat_message", "user", "apikey"]),
    ("Активность, документы, вложения", ["issue_activity", "project_document", "issue_attachment"]),
]

# Политика хранения таблиц проекта схемы (О-44): индексы, уникальность, срок, очистка, кто мигрирует.
# Индекс: (вид, колонки, зачем); вид — unique / index / hnsw. Сборка проверяет: у каждой таблицы есть политика,
# каждый FK покрыт индексом (первая колонка индекса или PK), срок ссылается на параметр спеки.
# Базы данных (D18, D22; data-methodology.md): кластер → база → схема. Таблица → «база.схема» — SCHEMA_OF.
DB_CLUSTER = dict(engine="PostgreSQL 17 + pgvector", operator="CloudNativePG", namespace="itsaplan-data", instances="1 (MVP, D18)",
                  pooler="PgBouncer (`Pooler` CloudNativePG), режим transaction", backup="WAL и базовые копии в S3 вне площадки (`postgres.backup`)",
                  roles="managed roles CloudNativePG (D22)")
DATABASES = {
    "itsaplan": dict(owner="icplan", schemas={
        "public": dict(owner="icplan", role="itsaplan", stores="S1", migrate="fork", what="таблицы форка, процесс задачи"),
        "platform": dict(owner="platform-module", role="itsaplan", stores="S2, S3", migrate="cp, obs",
                         what="настройки агентов, профили, доступы (Platform module); события запуска (Observability)"),
        "runner": dict(owner="agent-runner", role="runner", stores="S3", migrate="runner", what="слоты планировщика, кэш подготовки"),
        "harness_ckpt": dict(owner="agent-runner", role="runner", stores="S5", migrate="runner", what="checkpoint агентского цикла"),
        "memory": dict(owner="memory", role="memory", stores="S4", migrate="memory", what="M3, позже M4"),
    }),
    "litellm": dict(owner="llm-gateway", schemas={
        "public": dict(owner="llm-gateway", role="litellm", stores="S6", migrate="litellm", what="virtual keys, бюджеты, журнал затрат"),
    }),
}
# Чтение и ссылки на чужие таблицы — только явным GRANT (D22)
DB_GRANTS = [
    ("memory", "SELECT", "itsaplan.public.agent_run", "M2: итоги запусков"),
    ("memory", "SELECT", "itsaplan.public.agent_chat_message", "M1: переписка"),
    ("memory", "SELECT", "itsaplan.public.issue_activity", "M1, M2: комментарии и записи «агент взял / закончил» (D25)"),
    ("memory", "REFERENCES", "itsaplan.public.issue", "FK memory_m3.issue_id"),
    ("runner", "REFERENCES", "itsaplan.public.agent_run", "FK run_checkpoint.run_id, scheduler_slot"),
    ("litellm_read (api ICPlan)", "SELECT", "litellm.public.LiteLLM_SpendLogs", "Observability: затраты задачи"),
]
# Таблица платформы → «база.схема»; таблицы форка — itsaplan.public, LiteLLM — litellm.public
SCHEMA_OF = {
    "process": "itsaplan.public", "process_step": "itsaplan.public", "issue_process_state": "itsaplan.public", "agent_run_delivery": "itsaplan.public", "process_version": "itsaplan.public",
    "agent_settings": "itsaplan.platform", "agent_settings_version": "itsaplan.platform", "sandbox_profile": "itsaplan.platform",
    "memory_profile": "itsaplan.platform", "project_resource": "itsaplan.platform", "access_policy": "itsaplan.platform",
    "project_platform": "itsaplan.platform", "kill_switch": "itsaplan.platform", "run_event": "itsaplan.platform",
    "scheduler_slot": "itsaplan.runner", "setup_cache": "itsaplan.runner",
    "memory_m3": "itsaplan.memory", "m4_fact": "itsaplan.memory",
    "run_checkpoint": "itsaplan.harness_ckpt",
}

MIGRATE = {
    "fork": "Drizzle в форке (`packages/db`), применяются до старта `api`",
    "cp": "миграции Platform module в `api` форка, своя таблица версий, только схема `platform`",
    "obs": "миграции Observability в `api` форка, своя таблица версий",
    "runner": "миграции Agent Runner при старте, своя таблица версий",
    "memory": "миграции Memory API при старте (Alembic), своя таблица версий",
    "litellm": "миграции LiteLLM (Prisma) прямым подключением, минуя PgBouncer",
}
# таблицы форка, в которые пишет платформа (запуски, чат, история задачи): им тоже нужна политика (data-methodology)
FORK_WRITTEN = ["agent_run", "agent_chat_thread", "agent_chat_message", "issue_activity"]  # agent_chat_thread — удаляет worker по сроку D25

TABLE_POLICY = {
    # таблицы форка: индексы — как в схеме форка (None); срок и очистка — по коду форка (packages/db, apps/worker)
    "agent_run": (None, "завершённые — `runs.retention_days` = 365 по `finished_at` (icplan-integration, D25)", "каскадно с агентом, проектом, задачей; задача worker форка удаляет завершённые старше срока, запуски с `run_event` пропускает (R-ICP-19); для памяти M2 — фильтр чтения по `retention`, Memory не удаляет", "fork"),
    "agent_chat_message": (None, "тред — `chat.retention_days` = 90 по `updated_at` (icplan-integration, D25)", "каскадно с тредом и агентом; задача worker форка удаляет треды старше срока, сообщения и события — каскадом (R-ICP-19); для памяти M1 — фильтр чтения по `retention`", "fork"),
    "agent_chat_thread": (None, "`chat.retention_days` = 90 по `updated_at` (icplan-integration, D25)", "задача worker форка удаляет тред старше срока, сообщения и события (`agent_chat_message`, `agent_chat_event`) — каскадом (R-ICP-19); 0 — не чистить", "fork"),
    "issue_activity": (None, "пока жива задача (D25)", "каскадно с задачей; комментарий удаляется по одному; по времени не чистится — журнал задачи живёт с задачей (D25)", "fork"),
    "process": ([("unique", "project_id, issue_type_id", "один процесс на тип задачи"), ("index", "issue_type_id", "FK; процесс по типу задачи"), ("index", "first_step_id", "FK")],
                "пока жив проект", "каскадно с проектом; версия процесса растёт при правке", "fork"),
    "process_step": ([("unique", "process_id, key", "ключ шага уникален в процессе"), ("unique", "process_id, column_id", "одна колонка — один шаг"), ("index", "column_id", "FK; переход по колонке"), ("index", "agent_id", "FK; шаги агента")],
                     "пока жив процесс", "каскадно с процессом", "fork"),
    "issue_process_state": ([("index", "process_id, process_version", "FK; задачи на версии процесса"), ("index", "step_id, state", "задачи на шаге — доска и подхват")],
                            "пока жива задача", "каскадно с задачей", "fork"),
    "agent_settings": ([("index", "sandbox_profile_id", "FK"), ("index", "memory_profile_id", "FK")],
                       "пока жив агент", "каскадно с агентом", "cp"),
    "agent_settings_version": ([], "все версии (откат и аудит)", "каскадно с агентом", "cp"),
    "sandbox_profile": ([("unique", "name", "профиль по имени")], "бессрочно (справочник)", "удаление запрещено, пока профиль используется", "cp"),
    "memory_profile": ([("unique", "name", "профиль по имени")], "бессрочно (справочник)", "удаление запрещено, пока профиль используется", "cp"),
    "project_resource": ([("unique", "project_id, kind, ref", "ресурс один раз в проекте")], "пока жив проект", "каскадно с проектом", "cp"),
    "access_policy": ([("unique", "agent_id, resource_id", "одно право агента на ресурс"), ("index", "project_id", "FK"), ("index", "resource_id", "FK")],
                      "пока живы агент и ресурс", "каскадно", "cp"),
    "project_platform": ([], "пока жив проект", "каскадно с проектом", "cp"),
    "kill_switch": ([], "бессрочно (текущее состояние)", "история переключений — в аудите guardrails", "cp"),
    "scheduler_slot": ([("index", "run_id", "FK; освобождение по запуску"), ("index", "lease_until", "забор просроченных аренд")],
                       "на время аренды", "строка удаляется при освобождении; просроченная аренда (`lease_until`) забирается", "runner"),
    "run_event": ([("index", "ts", "очистка по сроку"), ("index", "issue_id, ts", "лента задачи")],
                  "`retention_days` = 90 (observability)", "ночная пакетная очистка по `ts`; при медленной очистке (этап 4) — секции по дням", "obs"),
    "setup_cache": ([("index", "project_id", "FK"), ("index", "expires_at", "очистка")],
                    "`setup.cache_ttl_h` = 168 (agent-sandbox)", "очистка по `expires_at` вместе с томом кэша", "runner"),
    "memory_m3": ([], "`memory.retention`: M3 до закрытия задачи (agent-memory)", "удаляется по профилю после закрытия задачи; M2 остаётся", "memory"),
    "m4_fact": ([("index", "superseded_by", "FK"), ("index", "scope, valid_to", "действующие факты области"), ("hnsw", "embedding", "поиск похожих (pgvector)")],
                "`memory.retention`: M4 до замены факта (agent-memory)", "заменённый факт получает `valid_to`, удаляется по профилю", "memory"),
    "agent_run_delivery": ([("index", "run_id", "FK; недоставленное по запуску"), ("index", "delivered_at", "выборка недоставленного")],
                           "пока жив запуск", "каскадно с `agent_run`; доставленное — со сроком `agent_run`", "fork"),
    "process_version": ([], "пока жив процесс", "каскадно с процессом", "fork"),
    "run_checkpoint": ([("index", "expires_at", "очистка")], "`checkpoint.ttl` = 7 дней (agent-harness)", "очистка по `expires_at`", "runner"),
}

STORES = {
    "icplan": ["S1", "S7"], "platform-module": ["S2"], "agent-runner": ["S3", "S5"], "memory": ["S4", "S1"], "observability": ["S3", "S6", "S1"],
    "llm-gateway": ["S6"], "mcp-tools": ["S1"], "guardrails": ["S11", "S8", "S2"], "sandbox": ["S10", "S7"], "harness": ["S10", "S5"],
    "infrastructure": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S9"],
}
# Нереляционные хранилища: схема-дерево
TREES = {
    "S7": ("RustFS, бакет `planner-attachments`", [
        "issues/<issue_id>/<public_id>        — вложения задач (issue_attachment)",
        "projects/<проект>/tasks/<задача>/<шаг>/v<N>/  — артефакты шагов, неизменяемые версии (D18)",
        "backups/postgres/                   — базовые копии и WAL (копия вне площадки)"]),
    "S10": ("`/workspace` в контейнере запуска", [
        "/workspace/repo/      — клон репозитория, ветка agent/<задача>",
        "/workspace/task/      — папка задачи (read), своя подпапка шага (write)",
        "/workspace/.deps/     — зависимости из шага подготовки (D19)"]),
    "S8": ("git", ["репозитории продукта — ветки agent/<задача>, PR", "репозиторий политик — Rego + тесты opa test"]),
    "S9": ("конфиг деплоя", ["values.yaml (git, без секретов) — параметры L0", "Secret / .env (вне git) — ключи, пароли"]),
    "S11": ("OPA в памяти", ["bundle = Rego (S8) + data.json из Platform module (OpaBundleData)"]),
}

# Структура эндпоинтов, которых нет в снимке OpenAPI форка, и доработок форка (О-45):
# «МЕТОД путь» (как в каталоге API) → (запрос, ответ, заметка). Модель — по имени (ссылка на поля), иначе — структура строкой.
# Эндпоинты, которые есть в OpenAPI форка, показываются из снимка автоматически; для 🛠 — снимок + эта запись.
ENDPOINT_IO = {
    # MCP ICPlan: смонтирован вне OpenAPI — apps/api/src/mcp/mount.ts форка
    "POST /mcp": ("JSON-RPC 2.0: `tools/list`, `tools/call` · `Authorization: Bearer <ключ агента>`", "200 · JSON-RPC result (MCP Streamable HTTP)", "путь вне OpenAPI форка: `app.ts` → `mountMcp` (`apps/api/src/mcp/mount.ts`); ключ — также `x-api-key`"),
    # Harness (API вызывает только Runner)
    "POST /run": ("RunBundle", "202 · {runId}", "запуск цикла; ответ сразу, ход — в `/run/events`"),
    "GET /run/events": ("query: seq — с какого события продолжить", "200 · NDJSON: RunEvent по строке", "переподключение без потерь по `seq`"),
    "POST /run/approval": ("ApprovalDecision", "204", ""),
    "POST /run/message": ("UserMessage", "204", ""),
    "POST /run/cancel": ("{reason}", "204", "Harness завершает шаг и отдаёт `RUN_FINISHED`"),
    "GET /ready": ("—", "200 · {ready, version}", "Runner ждёт готовности перед `POST /run`"),
    # Agent Runner
    "PUT /runs/:runId/checkpoint": ("Checkpoint", "204", "одноразовый токен запуска"),
    "GET /runs/:runId/checkpoint": ("query: iteration (нет — последняя)", "200 · Checkpoint", "при повторной выдаче запуска Harness продолжает с последней итерации"),
    "POST /runs/:runId/mcp/:server": ("McpToolCall", "200 · McpToolCall (result)", "allowlist запуска и G2 проверяются до вызова сервера"),
    "POST /runs/:runId/deps": ("{lockFiles?: string[]}", "200 · {status: ok · failed, log}", "повтор шага подготовки (D19)"),
    "GET /healthz": ("—", "200 · {status}", ""),
    # Guardrails (REST API OPA)
    "POST /v1/data/agent/g1": ("PolicyInput", "200 · PolicyDecision", "конверт `{input}` → `{result}` — REST API OPA"),
    "POST /v1/data/agent/g2": ("PolicyInput", "200 · PolicyDecision", ""),
    "GET /health?bundles": ("—", "200 · {}", "200 — бандл загружен (OPA)"),
    # ICPlan: доработки форка
    "PATCH /teams/:teamId/ai-agents/:agentId": ("+ {enabled: bool, onDisable: finish · cancel}", "как в форке", "к телу форка добавляем выключение агента (D17) и проверку модели у агента платформы (`kind = external`, R-REG-06): Platform module внутри api спрашивает LiteLLM `GET /model/info` (master key, I15), алиас `model` должен быть в `model_list`; ошибки: 400 — модель не настроена в LiteLLM `{field: model, reason}` (R-REG-06 «Модель без доступа»); 503 — LiteLLM недоступен, проверить модель нельзя: агент не сохраняется, прочие поля без смены модели сохраняются (R-REG-06 «Шлюз недоступен»); 403 — не администратор команды; 404 — агента нет"),
    "POST /agent-runs/:runId/heartbeat": ("—", "200 · Heartbeat (сейчас 204)", "тело ответа — доработка (D17, R-ICP-16); ошибки: 404 — запуск не найден, завершён или отменён (как в форке): это единственный сигнал отмены, Runner останавливает Harness и итог не шлёт (R-ICP-07)"),
    "POST /agent-runs/:runId/events": ("{events: RunEvent[]}", "204", "по образцу `POST /agent-chats/:messageId/events` форка (D21), но без `{canceled}`: отмену Runner узнаёт по 404 на heartbeat; ошибки: 404 — запуск не найден, не выдан этому ключу или уже завершён (отменён)"),
    "POST /agent-runs/:runId/result": ("RunResult (форк + `reason`, `artifacts`, `gate`, `criteriaNext`, `usage.reasoningTokens`, `usage.costUsd`, `usage.iterations`)", "204 (как в форке)", "ошибки (как в форке): 404 — запуск не найден, выдан другому агенту или уже завершён: `finishRun` обновляет только `pending`, поэтому повторная отправка итога и итог отменённого запуска — 404; Runner считает 404 на повтор доставленным итогом и не повторяет (R-ICP-13); 400 — тело не по схеме"),
    "GET /agent-runs/:runId/stream": ("—", "200 · SSE: `data: AgUiEvent`", "как `…/chat/:messageId/stream` форка (D21)"),
    "GET /issues/:issueId/agent-feed": ("—", "200 · {runs: {run: RunSummary, step, events: RunEvent[], result: RunResult}[]}", "история ленты по шагам процесса (D21)"),
    "POST /issues/:issueId/agent-verdict": ("Verdict", "204", "ошибки: 403 — нет права на задачу; 409 — нет итога, ждущего вердикта (R-AP-19)"),
    "PATCH /issues/:issueId": ("+ {reviewWithMe: bool}", "как в форке", "к телу форка добавляем флаг (R-AP-18); ошибки: 403 — нет права на задачу; смену колонки агентом в процессе ICPlan не применяет без ошибки, остальные поля обновляет (R-AP-16)"),
    "POST /issues/:issueId/process/pause": ("—", "204", "также `/resume`; ошибки: 403 — нет права; 409 — у задачи нет процесса или он уже в этом состоянии (R-AP-20)"),
    "POST /issues/:issueId/process/retry": ("{fromStep?: string}", "204", "ошибки: 403 — нет права; 409 — превышен `step.max_runs` или процесс остановлен (R-AP-21)"),
    "GET /issues/:issueId/agent-status": ("—", "200 · {state, queuePosition, waitReason}", "`state`: queued · running · waiting · paused · idle; `waitReason`: slot · approval · answer · runner_offline · agent_disabled (R-AP-07, R-AP-17)"),
    "GET /projects/:projectKey/processes": ("—", "200 · Process[]", ""),
    "POST /projects/:projectKey/actions": ("как в форке: {name, icon?, condition?, effect?}; `effect` — частичная правка задачи (`columnId`, `assigneeUserId`, `priority`, `typeId`, `startDate`, `dueDate`, `labelIds`) + {delegateUserId: string}",
                                           "201 · Action (как в форке)",
                                           "«делегировать агенту» (R-AP-03) — ключ `delegateUserId` = `user.id` бот-пользователя агента; API хранит `effect` как есть (`apps/api/src/modules/actions`), применяет его web одним `PATCH /issues/:issueId` (`apps/web/src/utils/actions.ts`), а делегат по коду форка ставит запуск `delegation`; доработка — ключ в `EFFECT_FIELD_KEYS` и редакторе эффекта, проверка агента при сохранении; ошибки: 400 — `delegateUserId` не агент проекта; 403 — нет права `actions.create`; при применении к выключенному агенту запуск не создаётся, запись в истории задачи (R-AP-03)"),
    "PUT /projects/:projectKey/processes/:issueTypeId": ("Process", "200 · Process (новая версия)", "ошибки: 400 — ошибка структуры `{step, reason}` (R-AP-15); 403 — не администратор проекта"),
    "POST /agent-runs/:runId/decisions": ("ApprovalDecision", "204", "решение пользователя по `seq` события; доставляется Runner в ответе heartbeat (R-ICP-05, R-ICP-16); ошибки: 403 — нет права `work_items.edit` в проекте задачи (D26); 409 — запуск завершён или решение уже есть"),
    "POST /agent-runs/:runId/messages": ("UserMessage", "204", "указание пользователя активному запуску; доставка — через heartbeat (R-ICP-16); ошибки: 403; 409 — запуск завершён"),
    "POST /agent-runs/:runId/cancel": ("—", "204", "отмена запуска по задаче; Runner узнаёт по 404 на heartbeat (R-ICP-07); ошибки: 403; 409 — запуск уже завершён; для запусков по расписанию в форке есть `…/agent-schedules/:scheduleId/runs/:runId/cancel`"),
    "GET /issues/:issueId/costs": ("—", "200 · CostAggregate[] (по агентам задачи)", "журнал затрат LiteLLM по `run_id` (I14, роль `litellm_read`); `costUsd = null`, если цена не задана; журнал недоступен — тоже 200: `runs` из `agent_run`, токены и `costUsd` = `null`, экран показывает «неизвестно» (R-OBS-05)"),
    "GET /me/agent-summary": ("—", "200 · {working, queued, waitingMe: {issueId, issueIdentifier, agentId, since}[], costUsd}", ""),
    "POST /mcp": ("McpToolCall", "200 · McpToolCall (result)", "MCP-сервер ICPlan, не в OpenAPI"),
    # LiteLLM
    "POST /v1/chat/completions": ("ChatCompletionRequest", "200 · ответ OpenAI Chat Completions (`choices`, `usage`)", "mock — тот же формат"),
    "GET /model/info": ("—", "200 · {data: {model_name, litellm_params, model_info}[]}", "проверка алиаса модели при сохранении агента (R-REG-06); вызывает Platform module master key (I15)"),
    "POST /key/generate": ("VirtualKey", "200 · {key, key_alias, expires}", "также `/key/update`"),
    "GET /spend/logs": ("query: request_id или start_date / end_date", "200 · LiteLLM_SpendLogs[]", "отбор по `metadata.run_id`"),
    # MCP
    "POST tools/list": ("McpToolCall (method tools/list)", "200 · {tools: {name, description, inputSchema}[]}", "JSON-RPC 2.0"),
    "POST tools/call": ("McpToolCall", "200 · McpToolCall (result)", ""),
    # Memory API
    "GET /context": ("query: issueId, agentId", "200 · {m1: UserMessage[], m2: RunSummary[], m3: M3Record, m5, m6}", "по профилю памяти агента"),
    "PUT /m3/:issueId": ("M3Record", "200 · M3Record (новая version)", "409 — запись изменилась (конкурентная запись)"),
    "DELETE /records/:level/:id": ("—", "204", ""),
    "POST /retention/run": ("—", "200 · {deleted: {m3}}", "CronJob; M4 — после MVP; M1 и M2 в таблицах форка не удаляет — фильтр чтения, строки удаляет ICPlan (D25)"),
    # Platform module
    "GET /platform/agents/:agentId/settings": ("—", "200 · AgentSettings", ""),
    "PATCH /platform/agents/:agentId/settings": ("AgentSettings (часть полей)", "200 · AgentSettings (новая version)", "со следующего запуска"),
    "GET /platform/agents/:agentId/export": ("—", "200 · YAML определения агента", ""),
    "POST /platform/agents/import": ("YAML определения агента", "200 · {agentId, version}", ""),
    "PUT /platform/projects/:projectKey/guidance": ("{guidance: string}", "204", ""),
    "PUT /platform/projects/:projectKey/budget": ("{monthUsd: number}", "204", ""),
    "GET /platform/projects/:projectKey/access": ("—", "200 · {agentId, resourceId, right}[]", ""),
    "PUT /platform/projects/:projectKey/access": ("{agentId, resourceId, right}[]", "204", ""),
    "GET /platform/agents/:agentId/settings/versions": ("—", "200 · {version, by, at}[]", "история настроек (R-CP-04)"),
    "POST /platform/agents/:agentId/settings/rollback": ("{version: int}", "200 · AgentSettings (новая version)", "новая версия с содержимым выбранной, со следующего запуска (R-CP-04); ошибки: 403 — нет права `ai_agents`"),
    "GET /platform/kill-switch": ("—", "200 · {scope, enabled, reason, by, at}[]", "`scope`: `platform` · `agent:<id>` (`kill_switch`)"),
    "PUT /platform/kill-switch/:scope": ("{enabled: bool, reason}", "204", "действует сразу (R-CP-03, R-GRD-15); `agent:<id>` — право `ai_agents`, `platform` — владелец экземпляра; API — и для эксплуатации (D24); ошибки: 403 — нет права на эту область"),
    "GET /platform/sandbox-profiles": ("—", "200 · {id, name, image, runtime, cpu, memoryMb, diskGb, egressAllow, poolSize}[]", "`sandbox_profile`"),
    "PUT /platform/sandbox-profiles/:name": ("{image, runtime, cpu, memoryMb, diskGb, egressAllow, poolSize}", "204", "владелец экземпляра (D24); удаление — `DELETE`, запрещено, пока профиль используется; ошибки: 400 — недопустимое значение с указанием поля (R-CP-01); 403 — не владелец экземпляра"),
    "DELETE /platform/sandbox-profiles/:name": ("—", "204", "ошибки: 403 — не владелец экземпляра; 404 — профиля нет; 409 — профиль используется: в ответе агенты с этим профилем (`agent_settings.sandbox_profile_id`)"),
    "GET /platform/memory-profiles": ("—", "200 · {id, name, read, write, m2LastRuns, retention, scope}[]", "`memory_profile`"),
    "PUT /platform/memory-profiles/:name": ("{read, write, m2LastRuns, retention, scope}", "204", "владелец экземпляра (D24); удаление — `DELETE`, запрещено, пока профиль используется; ошибки: 400 — недопустимое значение с указанием поля (R-CP-01); 403 — не владелец экземпляра"),
    "DELETE /platform/memory-profiles/:name": ("—", "204", "ошибки: 403 — не владелец экземпляра; 404 — профиля нет; 409 — профиль используется: в ответе агенты с этим профилем (`agent_settings.memory_profile_id`)"),
    "GET /platform/projects/:projectKey": ("—", "200 · {guidance, budgetMonthUsd, setupScript, lockFiles}", "`project_platform`; строки нет — пустые значения; ошибки: 403 — нет права `ai_agents` в проекте; 404 — проекта нет"),
    "GET /platform/projects/:projectKey/resources": ("—", "200 · {id, kind, ref, name}[]", "`project_resource`: `kind` — git · folder · document · mcp"),
    "PUT /platform/projects/:projectKey/resources": ("{kind, ref, name}[]", "204", "право `ai_agents` в разделе проекта (D24); ошибки: 403 — нет права (R-CP-07)"),
    "PUT /platform/projects/:projectKey/setup": ("{setupScript: string, lockFiles: string[]}", "204", "шаг подготовки (D19), `project_platform`; ошибки: 403 — нет права `ai_agents` (R-CP-07)"),
    "GET /platform/runs/:runId/manifest": ("—", "200 · WorkspaceSource[]", "для Runner"),
    "GET /platform/runs/:runId/agent": ("—", "200 · {version, definition: AgentDefinition, settings: AgentSettings}", "для Runner (I4, D23): вызов при старте после слотов; версию пишет в `agent_run.agent_version` при первом вызове, повтор — та же; ошибки: 404 — запуск не `pending` или агент не `external`; 409 — версии нет (R-REG-03)"),
    "GET /platform/audit": ("query: from, to, entity", "200 · {at, by, entity, change}[]", "чтение — владелец экземпляра и Безопасность (US-PM-07, D24)"),
    # Sandbox, инфраструктура — внешние API
    "POST Docker": ("Docker Engine API `POST /containers/create` (образ, ресурсы профиля, сеть)", "201 · {Id}", "через docker-socket-proxy"),
    "DELETE Docker": ("Docker Engine API `DELETE /containers/:id`", "204", ""),
    "POST Kubernetes": ("Kubernetes API: Pod из `SandboxClaim`", "201 · Pod", "этап 4"),
    "GET https://<домен>/": ("—", "200 · web ICPlan", ""),
    "GET https://<домен>/api/*": ("—", "как api ICPlan", ""),
}


# Доработки колонок форка ICPlan (Z-ICP-10, Z-ICP-13, Z-ICP-14): таблица → [(колонка, тип, ключ, описание)].
# Показываются на «Данных» вместе с колонками схемы форка, с пометкой доработки.
FORK_COLUMNS = {
    "issue": [("review_with_me", "bool", "", "🛠 проверять со мной все шаги (D17, R-AP-18)")],
    "ai_agent": [("enabled", "bool", "", "🛠 агент включён: создаются и выдаются запуски (D17, R-ICP-17)")],
    "issue_checklist_item": [("origin", "text", "", "🛠 кто задал критерий: process · user:<username> · agent:<username> · reviewer:<username> (D20)"),
                             ("status", "text", "", "🛠 active · pending_approval (D20)")],
    "agent_run": [("process_step_id", "int", "FK process_step", "🛠 шаг процесса запуска — `Run.rule.stepId` (D17)"),
                  ("agent_version", "int", "", "🛠 версия определения агента запуска (R-REG-03): задаёт задача или Platform module при первом вызове `GET /platform/runs/:runId/agent` (D23)"),
                  ("reason", "text", "", "🛠 причина итога — `RunResult.reason` (R-RUN-07)"),
                  ("artifacts", "jsonb", "", "🛠 опубликованное — `RunResult.artifacts` (D20)"),
                  ("gate", "jsonb", "", "🛠 проверка по критериям — `RunResult.gate` (D20)"),
                  ("reasoning_tokens", "int", "", "🛠 `RunResult.usage.reasoningTokens` (D18)"),
                  ("iterations", "int", "", "🛠 `RunResult.usage.iterations` (D18)"),
                  ("cost_usd", "numeric", "", "🛠 `RunResult.usage.costUsd`; null — неизвестна (R-OBS-05)")],
}
