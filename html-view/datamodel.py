"""Интеграции, контракты и модель данных компонентов — единый источник для карточек и страницы «Модель данных».

Источники:
- интерфейсы I1–I23 — матрица docs/flows/data-types.md и таблицы «Интерфейсы обмена» в interfaces.md спек;
- эндпоинты — страницы каталога docs/api/*.md (сборка читает их сама);
- таблицы ICPlan — код форка, packages/db/src/schema/app.ts (icplan_schema.json + .meta.json с коммитом; обновлять: python html-view/schema_import.py [путь к форку], сборка сверяет коммит);
- таблицы платформы — проект схемы по спекам и решениям D4, D17–D20 (до реализации);
- таблицы LiteLLM — schema.prisma тега v1.104.2 (LITELLM_REF; колонки и типы сверены 2026-10-11).
Правило: docs/rules/change-process.md (новый интерфейс, хранилище или модель → этот файл).
"""

# ---------- интеграции ----------
# I-код → (от, к, через, что передаётся, модели). Слаги компонентов или внешние участники в «…».
INTEG = {
    "I1": ("icplan", "agent-runner", "", "выдача запуска из очереди агента (pull, аренда)", ["Run"]),
    "I2": ("agent-runner", "icplan", "", "шаги запуска и итог", ["RunEvent", "RunResult"]),
    "I3": ("icplan", "agent-runner", "", "подтверждения, отмена, указания — в ответе heartbeat", ["Heartbeat", "ApprovalDecision", "UserMessage"]),
    "I4": ("agent-runner", "platform-module", "", "настройки агента и манифест рабочего пространства", ["AgentSettings", "WorkspaceSource"]),
    "I5": ("agent-runner", "guardrails", "", "допуск запуска G1", ["PolicyInput", "PolicyDecision"]),
    "I6": ("agent-runner", "sandbox", "", "создание и уничтожение среды (Docker API)", ["SandboxClaim", "RepoGrant"]),
    "I7": ("agent-runner", "harness", "", "задание, события, подтверждения, итог", ["RunBundle", "RunEvent", "ApprovalDecision", "RunResult"]),
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
    "I20": ("icplan", "icplan", "", "интерфейс ICPlan ↔ API (в том числе экраны Platform module, таймлайн, сводка)", ["Process", "Verdict", "CostAggregate"]),
    "I21": ("«пользователи»", "icplan", "infrastructure", "вход по HTTPS через Traefik: web, api, mcp", []),
    "I22": ("«сервисы»", "infrastructure", "", "Postgres через PgBouncer", []),
    "I23": ("agent-runner", "sandbox", "infrastructure", "среды запусков через Kubernetes API (этап 4)", ["SandboxClaim"]),
}
# Кто пользуется общими стыками I22 (БД) и I20 (API ICPlan), кроме владельцев
ALSO = {"I22": ["icplan", "platform-module", "agent-runner", "memory", "observability", "llm-gateway"],
        "I20": ["platform-module", "observability"], "I2": ["observability", "memory"], "I14": ["observability"],
        "I19": ["sandbox", "icplan"], "I17": ["sandbox", "mcp-tools"],
        "I8": ["guardrails"], "I7": ["sandbox"], "I18": ["sandbox"]}

# ---------- модели обмена ----------
# имя → (назначение, [(поле, тип, обязательное, описание)])
MODELS = {
    "Run": ("выдача запуска из очереди ICPlan (`POST /agent-runs/claim`)", [
        ("id", "int", True, "идентификатор `agent_run.id`"), ("agentId", "int", True, "агент"),
        ("issue", "{key, title, url}", False, "задача; нет — запуск по расписанию или чату"),
        ("trigger", "enum: delegation · mention · schedule · field · process_step · manual", True, "что создало запуск"),
        ("prompt", "string", True, "задание"), ("rule", "{type, process, step}", False, "правило автоподхвата (D17)")]),
    "Heartbeat": ("продление аренды и обратный канал (`POST /agent-runs/:id/heartbeat`)", [
        ("active", "bool", True, "`false` — запуск отменён, Runner останавливает"),
        ("approvals", "ApprovalDecision[]", False, "решения пользователя"), ("messages", "UserMessage[]", False, "указания во время работы (D18)")]),
    "RunBundle": ("задание Harness (`POST /run`)", [
        ("runId", "int", True, "запуск"), ("agent", "{model, version, instruction, skills[]}", True, "определение агента версии запуска"),
        ("guidance", "string", False, "руководство проекта"), ("params", "map<string, any>", True, "параметры L0–L3 (`model.*`, `limits.*`)"),
        ("workspace", "WorkspaceSource[]", False, "манифест рабочего пространства (R-RUN-17)"),
        ("memory", "{m3: M3Record, m2: RunSummary[]}", False, "память для продолжения"),
        ("task", "{key, criteria: Criterion[], returnNote}", False, "задача, критерии с происхождением (D20), заметка возврата"),
        ("mcp", "{server, url, tools[]}[]", False, "MCP через прокси Runner (D19)")]),
    "WorkspaceSource": ("источник рабочего пространства", [
        ("name", "string", True, "имя в `/workspace/<имя>`"), ("type", "enum: git · folder", True, "вид"),
        ("url / prefix", "string", True, "репозиторий или префикс в RustFS"), ("branch", "string", False, "ветка агента `agent/<задача>`"),
        ("right", "enum: read · write · handoff", True, "право по политике (D18)")]),
    "Criterion": ("критерий приёмки (D20)", [
        ("text", "string", True, "проверяемая формулировка"), ("origin", "enum: process · user:<имя> · agent:<шаг> · reviewer:<кто>", True, "происхождение"),
        ("status", "enum: active · pending_approval", True, "ждёт подтверждения по `criteria_approval`")]),
    "RunEvent": ("событие запуска: конверт платформы вокруг события AG-UI (D21; NDJSON `/run/events`, `POST /agent-runs/:runId/events`)", [
        ("runId", "int", True, "запуск, = `agent_run.id`"), ("seq", "int", True, "порядковый номер от Harness; ключ идемпотентности и порядка"),
        ("at", "timestamp", True, "время события в Harness"),
        ("event", "AgUiEvent", True, "событие AG-UI как есть: `type` и поля протокола")]),
    "AgUiEvent": ("событие протокола AG-UI (docs.ag-ui.com; то же, что принимает чат агента форка)", [
        ("type", "enum: RUN_STARTED · RUN_FINISHED · RUN_ERROR · STEP_STARTED · STEP_FINISHED · TEXT_MESSAGE_START · TEXT_MESSAGE_CONTENT · TEXT_MESSAGE_END · REASONING_START · REASONING_MESSAGE_START · REASONING_MESSAGE_CONTENT · REASONING_MESSAGE_END · REASONING_END · TOOL_CALL_START · TOOL_CALL_ARGS · TOOL_CALL_END · TOOL_CALL_RESULT · ACTIVITY_SNAPSHOT · CUSTOM", True, "тип события по протоколу"),
        ("runId / threadId", "string", False, "у `RUN_*`: запуск и тред (тред = задача)"), ("stepName", "string", False, "у `STEP_*`: шаг цикла"),
        ("messageId / role / delta", "string", False, "у `TEXT_MESSAGE_*`, `REASONING_MESSAGE_*`: сообщение, роль, фрагмент текста"),
        ("toolCallId / toolCallName / parentMessageId / content", "string", False, "у `TOOL_CALL_*`: вызов тула, имя, сообщение-родитель, результат"),
        ("activityType / content", "string / object", False, "у `ACTIVITY_SNAPSHOT`: `plan` и содержимое плана"),
        ("name", "string", False, "у `CUSTOM`: `question`, `approval_request`, `guardrail_decision`, `memory_write`, `llm_call`"), ("value", "object", False, "у `CUSTOM`: данные события по `name`"),
        ("message / code", "string", False, "у `RUN_ERROR`: причина")]),
    "RunResult": ("итог запуска (`POST /agent-runs/:id/result`)", [
        ("status", "enum: success · failed · canceled", True, "статус ICPlan (R-RUN-07 → ICPlan)"), ("reason", "enum: done · limit · gate_failed · error", False, "причина Harness"),
        ("output", "markdown", True, "итог для задачи"), ("artifacts", "{name, url}[]", False, "опубликованные файлы, ветка, PR"),
        ("gate", "{passed, failed[]}", False, "результат quality gate (R-HRN-08)"),
        ("usage", "{prompt_tokens, completion_tokens, reasoning_tokens, cost_usd, steps}", True, "расход")]),
    "ApprovalDecision": ("решение пользователя по паузе", [
        ("runId", "int", True, ""), ("seq", "int", True, "`seq` события `CUSTOM` `approval_request` или `question`"), ("decision", "enum: approve · reject · answer", True, ""),
        ("scope", "enum: once · run", False, "только этот вызов или до конца запуска (R-GRD-03)"), ("by", "string", True, "кто решил"), ("comment", "string", False, "")]),
    "UserMessage": ("указание пользователя во время работы", [
        ("id", "string", True, ""), ("text", "string", True, ""), ("by", "string", True, ""), ("at", "timestamp", True, "")]),
    "Verdict": ("вердикт по результату шага (R-AP-19)", [
        ("runId", "int", True, ""), ("verdict", "enum: accepted · rejected", True, ""), ("note", "string", False, "заметка возврата"),
        ("criteria", "Criterion[]", False, "критерии ревьюера при возврате (D20)")]),
    "Process": ("процесс типа задачи (D17)", [
        ("issueType", "string", True, "тип задачи"), ("owner", "string", True, "владелец процесса"), ("firstStep", "string", True, ""),
        ("steps", "ProcessStep[]", True, "шаги"), ("version", "int", True, "версия процесса")]),
    "ProcessStep": ("шаг процесса (D17, D20)", [
        ("id", "string", True, ""), ("column", "string", True, "колонка проекта"), ("agent", "string", False, "агент шага; нет — ручной шаг"),
        ("onSuccess / onFailure", "{step | process | done}", True, "переходы по итогу"), ("maxRuns", "int", True, "лимит запусков, по умолчанию 3"),
        ("requireReview", "bool", True, "проверка человеком"), ("deliverable", "string", False, "результат шага (D20)"),
        ("doneCriteria", "Criterion[]", False, "готовность шага (D20)"), ("criteriaApproval", "enum: auto · review · always", True, "подтверждение критериев агента (D20)")]),
    "M3Record": ("состояние задачи и передача следующему шагу (R-MEM-04, D20)", [
        ("issue_key", "string", True, ""), ("scope", "enum: issue · agent · project · team", True, "область"), ("agent", "string", True, "автор"),
        ("done", "string[]", True, "сделано"), ("next", "string[]", True, "дальше"), ("blockers", "string[]", False, ""),
        ("artifacts", "{path, ref}[]", False, "артефакты: путь и ветка@коммит"), ("questions", "string[]", False, "открытые вопросы"),
        ("criteria_next", "Criterion[]", False, "критерии, предложенные следующему шагу")]),
    "PolicyInput": ("вход OPA (G1, G2)", [
        ("point", "enum: g1 · g2", True, ""), ("agent", "string", True, ""), ("run", "{id, issue, step}", True, ""),
        ("tool / args_hash", "string", False, "для G2"), ("autonomy", "enum: R0–R5", True, "уровень автономии"), ("budget", "{run, day, month}", False, "для G1")]),
    "PolicyDecision": ("решение OPA", [
        ("allow", "bool", True, ""), ("approval", "bool", True, "нужна пауза на подтверждение"), ("reason", "string", True, "причина для аудита")]),
    "AgentSettings": ("настройки агента из Platform module (I4)", [
        ("agentId", "int", True, ""), ("version", "int", True, "версия настроек (R-CP-04)"), ("autonomy", "enum: R0–R5", True, ""),
        ("budget", "{run_usd, day_usd}", True, ""), ("sandboxProfile", "SandboxProfile", True, ""), ("memoryProfile", "MemoryProfile", True, ""),
        ("toolsAllow / approvalTools", "string[]", True, "данные guardrails"), ("scheduling", "{parallel, max}", False, ""), ("enabled", "bool", True, "выключение агента")]),
    "SandboxClaim": ("заявка на среду запуска", [
        ("profile", "string", True, ""), ("sandbox_id", "string", True, ""), ("image", "string", True, "образ Harness"),
        ("runtime", "enum: runc · runsc", True, "D19 / R-SBX-05"), ("cpu / memory_mb / disk_gb", "number", True, ""), ("ready_ms", "int", False, "время готовности")]),
    "RepoGrant": ("доступ к репозиторию на один запуск", [
        ("repo", "string", True, ""), ("access", "enum: read · write", True, ""), ("branch_prefix", "string", True, "`agent/<задача>`"),
        ("protected", "string[]", True, "ветки без записи"), ("ttl_s", "int", True, "срок токена")]),
    "Checkpoint": ("состояние цикла (I12)", [
        ("runId", "int", True, ""), ("step", "int", True, "ключ идемпотентности"), ("parent_step", "int", False, ""),
        ("state", "bytes", True, "сериализованное состояние графа LangGraph")]),
    "ChatCompletionRequest": ("запрос к модели (OpenAI Chat Completions)", [
        ("model", "string", True, "алиас из `model_list`"), ("messages", "{role, content}[]", True, "слои промпта (R-HRN-18)"), ("tools", "{type, function: {name, parameters}}[]", False, ""),
        ("tool_choice / parallel_tool_calls", "enum / bool", False, "Harness: `auto`, без параллельных вызовов"), ("temperature / max_tokens / reasoning_effort", "number / enum", False, "`model.*`; неподдерживаемое отбрасывает `drop_params`"),
        ("metadata", "{run_id, issue_key, agent}", True, "атрибуция затрат (R-LLM-03)"), ("stream", "bool", False, "")]),
    "McpToolCall": ("вызов тула MCP (JSON-RPC 2.0)", [
        ("jsonrpc / id", "string / int", True, "конверт JSON-RPC 2.0"), ("method", "enum: tools/list · tools/call", True, ""), ("params.name", "string", False, "имя тула"), ("params.arguments", "object", False, "аргументы"),
        ("result.content", "{type, text}[]", False, "результат, обрезка `max_result_kb`")]),
    "VirtualKey": ("ключ LiteLLM на агента (`/key/generate`)", [
        ("key_alias", "string", True, "`agent:<id>`"), ("models", "string[]", True, "разрешённые алиасы"), ("max_budget", "float", True, "бюджет $"),
        ("budget_duration", "string", True, "период"), ("rpm_limit / tpm_limit", "int", False, ""), ("metadata", "object", False, "")]),
    "CostAggregate": ("сводка затрат по задаче и агенту (экран «Затраты», R-OBS-03)", [
        ("issue_key", "string", True, "ключ задачи"), ("agent", "string", True, "агент"), ("runs", "int", True, "число запусков"),
        ("prompt_tokens / completion_tokens", "int", True, "токены из журнала LiteLLM"), ("cost_usd", "float", True, "затраты")]),
    "OpaBundleData": ("данные бандла OPA (`data.json`)", [
        ("agents.<id>.tools_allow", "string[]", True, ""), ("agents.<id>.approval", "string[]", True, "тулы с паузой"),
        ("agents.<id>.autonomy", "enum: R0–R5", True, ""), ("agents.<id>.budget", "{run, day}", True, ""), ("platform.kill_switch", "bool", True, "")]),
}

# ---------- хранилища ----------
# Таблицы ICPlan из кода форка: компонент → [(ключ в icplan_schema.json, пометка)]
ICPLAN_TABLES = {
    "icplan": [("project", ""), ("projectColumn", ""), ("issueType", ""), ("issue", "+ `review_with_me` (D17)"), ("issueChecklist", ""),
               ("issueChecklistItem", "+ `origin`, `status` (D20)"), ("issueActivity", ""), ("aiAgent", "+ `enabled` (D17)"), ("agentRun", ""),
               ("agentSchedule", ""), ("agentChatThread", ""), ("agentChatMessage", ""), ("projectAction", "+ эффект `delegate_agent`"),
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
    "process_step": ("S1", "icplan", [("id", "serial", "PK", ""), ("process_id", "int", "FK process", ""), ("column_id", "int", "FK project_column", "колонка"),
                                      ("agent_id", "int", "FK ai_agent", "нет — ручной шаг"), ("on_success", "jsonb", "", "шаг / процесс / завершить"), ("on_failure", "jsonb", "", ""),
                                      ("max_runs", "int", "", "3"), ("require_review", "bool", "", ""), ("deliverable", "text", "", "результат шага (D20)"),
                                      ("done_criteria", "jsonb", "", "готовность шага (D20)"), ("criteria_approval", "text", "", "auto / review / always")]),
    "issue_process_state": ("S1", "icplan", [("issue_id", "int", "PK, FK issue", ""), ("process_id", "int", "FK process", ""), ("step_id", "int", "FK process_step", "текущий шаг"),
                                             ("runs_on_step", "int", "", "счётчик для `max_runs`"), ("state", "text", "", "running / waiting_review / paused / done"),
                                             ("last_verdict", "text", "", "accepted / rejected"), ("updated_at", "timestamptz", "", "")]),
    "agent_settings": ("S2", "platform-module", [("agent_id", "int", "PK, FK ai_agent", ""), ("version", "int", "", "текущая версия"), ("autonomy_level", "text", "", "R0–R5"),
                                                 ("budget_run_usd", "numeric", "", ""), ("budget_day_usd", "numeric", "", ""), ("sandbox_profile_id", "int", "FK sandbox_profile", ""),
                                                 ("memory_profile_id", "int", "FK memory_profile", ""), ("tools_allow", "jsonb", "", ""), ("approval_tools", "jsonb", "", ""),
                                                 ("scheduling", "jsonb", "", "parallel, max"), ("updated_by", "text", "", ""), ("updated_at", "timestamptz", "", "")]),
    "agent_settings_version": ("S2", "platform-module", [("agent_id", "int", "PK, FK agent_settings", ""), ("version", "int", "PK", ""), ("data", "jsonb", "", "снимок настроек"),
                                                         ("created_by", "text", "", ""), ("created_at", "timestamptz", "", "")]),
    "sandbox_profile": ("S2", "platform-module", [("id", "serial", "PK", ""), ("name", "text", "", "light, coder…"), ("image", "text", "", ""), ("runtime", "text", "", "runc / runsc"),
                                                  ("cpu", "numeric", "", ""), ("memory_mb", "int", "", ""), ("disk_gb", "int", "", ""), ("egress_allow", "jsonb", "", ""), ("pool_size", "int", "", "")]),
    "memory_profile": ("S2", "platform-module", [("id", "serial", "PK", ""), ("name", "text", "", ""), ("read", "jsonb", "", "уровни"), ("write", "jsonb", "", ""),
                                                 ("m2_last_runs", "int", "", "3"), ("retention", "jsonb", "", ""), ("scope", "text", "", "задача…")]),
    "project_resource": ("S2", "platform-module", [("id", "serial", "PK", ""), ("project_id", "int", "FK project", ""), ("kind", "text", "", "git / folder / document / mcp"),
                                                   ("ref", "text", "", "адрес, префикс, id"), ("name", "text", "", "")]),
    "access_policy": ("S2", "platform-module", [("id", "serial", "PK", ""), ("project_id", "int", "FK project", ""), ("agent_id", "int", "FK ai_agent", ""),
                                                ("resource_id", "int", "FK project_resource", ""), ("right", "text", "", "read / write / handoff"), ("template_role", "text", "", "шаблон по роли агента")]),
    "project_platform": ("S2", "platform-module", [("project_id", "int", "PK, FK project", ""), ("guidance", "text", "", "руководство проекта"), ("budget_month_usd", "numeric", "", ""),
                                                   ("setup_script", "text", "", "шаг подготовки (D19)"), ("lock_files", "jsonb", "", "для кэша")]),
    "kill_switch": ("S2", "platform-module", [("scope", "text", "PK", "platform / agent:<id>"), ("enabled", "bool", "", ""), ("reason", "text", "", ""), ("by", "text", "", ""), ("at", "timestamptz", "", "")]),
    "scheduler_slot": ("S3", "agent-runner", [("slot_key", "text", "PK", "global:N / agent:<id> / model:<alias> / issue:<id>"), ("run_id", "int", "FK agent_run", ""),
                                              ("runner_id", "text", "", "экземпляр Runner"), ("lease_until", "timestamptz", "", "аренда слота"), ("acquired_at", "timestamptz", "", "")]),
    "run_event": ("S3", "observability", [("run_id", "int", "PK, FK agent_run", "целое, как `agent_run.id`"), ("seq", "int", "PK", ""), ("ts", "timestamptz", "", ""),
                                          ("type", "text", "", "`event.type` AG-UI, для отбора"), ("event", "jsonb", "", "событие AG-UI целиком, маскированное; дельты собраны в сообщение"), ("issue_key", "text", "", "")]),
    "setup_cache": ("S3", "agent-runner", [("lock_hash", "text", "PK", "хеш lock-файлов"), ("project_id", "int", "FK project", ""), ("path", "text", "", "том кэша"),
                                           ("created_at", "timestamptz", "", ""), ("expires_at", "timestamptz", "", "`setup.cache_ttl_h`")]),
    "memory_m3": ("S4", "memory", [("issue_id", "int", "PK, FK issue", ""), ("scope", "text", "PK", ""), ("agent", "text", "", "автор"), ("done", "jsonb", "", ""), ("next", "jsonb", "", ""),
                                   ("blockers", "jsonb", "", ""), ("artifacts", "jsonb", "", "D20"), ("questions", "jsonb", "", "D20"), ("criteria_next", "jsonb", "", "D20"),
                                   ("version", "int", "", ""), ("updated_at", "timestamptz", "", "")]),
    "m4_fact": ("S4", "memory", [("id", "bigserial", "PK", "после MVP"), ("scope", "text", "", ""), ("text", "text", "", "маскированный"), ("embedding", "vector", "", "pgvector"),
                                 ("source", "text", "", ""), ("valid_from", "timestamptz", "", ""), ("valid_to", "timestamptz", "", ""), ("superseded_by", "bigint", "FK m4_fact", "")]),
    "run_checkpoint": ("S5", "agent-runner", [("run_id", "int", "PK, FK agent_run", ""), ("step", "int", "PK", ""), ("parent_step", "int", "", ""), ("state", "bytea", "", "состояние LangGraph"),
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
MIGRATE = {
    "fork": "Drizzle в форке (`packages/db`), применяются до старта `api`",
    "cp": "миграции Platform module в `api` форка, своя таблица версий, только схема `platform`",
    "obs": "миграции Observability в `api` форка, своя таблица версий",
    "runner": "миграции Agent Runner при старте, своя таблица версий",
    "memory": "миграции Memory API при старте (Alembic), своя таблица версий",
}
TABLE_POLICY = {
    "process": ([("unique", "project_id, issue_type_id", "один процесс на тип задачи"), ("index", "issue_type_id", "FK; процесс по типу задачи"), ("index", "first_step_id", "FK")],
                "пока жив проект", "каскадно с проектом; версия процесса растёт при правке", "fork"),
    "process_step": ([("unique", "process_id, column_id", "одна колонка — один шаг"), ("index", "column_id", "FK; переход по колонке"), ("index", "agent_id", "FK; шаги агента")],
                     "пока жив процесс", "каскадно с процессом", "fork"),
    "issue_process_state": ([("index", "process_id", "FK"), ("index", "step_id, state", "задачи на шаге — доска и подхват")],
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
    "run_event": ([("index", "ts", "очистка по сроку"), ("index", "issue_key, ts", "таймлайн задачи")],
                  "`retention_days` = 90 (observability)", "ночная пакетная очистка по `ts`; при медленной очистке (этап 4) — секции по дням", "obs"),
    "setup_cache": ([("index", "project_id", "FK"), ("index", "expires_at", "очистка")],
                    "`setup.cache_ttl_h` = 168 (agent-sandbox)", "очистка по `expires_at` вместе с томом кэша", "runner"),
    "memory_m3": ([], "`memory.retention`: M3 до закрытия задачи (agent-memory)", "удаляется по профилю после закрытия задачи; M2 остаётся", "memory"),
    "m4_fact": ([("index", "superseded_by", "FK"), ("index", "scope, valid_to", "действующие факты области"), ("hnsw", "embedding", "поиск похожих (pgvector)")],
                "`memory.retention`: M4 до замены факта (agent-memory)", "заменённый факт получает `valid_to`, удаляется по профилю", "memory"),
    "run_checkpoint": ([("index", "expires_at", "очистка")], "`checkpoint.ttl` = 7 дней (agent-harness)", "очистка по `expires_at`", "runner"),
}

STORES = {
    "icplan": ["S1"], "platform-module": ["S2"], "agent-runner": ["S3", "S5"], "memory": ["S4", "S1"], "observability": ["S3", "S6", "S1"],
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
