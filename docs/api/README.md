# Каталог API

← [Справка](../HOW-TO-READ.md) · [типы данных](../flows/data-types.md) · [сборка запроса к модели](../flows/harness.md#llm-request)

Все API, которые нужны историям: что уже есть в ICPlan, что дорабатываем в форке и что делаем в сервисах платформы. У каждого вызова — кто вызывает, аутентификация, истории, требования и интерфейс (I-код).

<div class="api-legend"><span class="st st-ok">✅ есть</span> <span class="st st-fork">🛠 доработка форка</span> <span class="st st-new">🆕 новое</span></div>

| Компонент | Базовый адрес | Аутентификация | ✅ | 🛠 | 🆕 |
|---|---|---|---|---|---|
| [ICPlan (форк)](icplan.md) | `https://<домен>/api` (api ICPlan, порт 3000) | UI — сессия пользователя; агент и Runner — `Authorization: Bearer <ключ агента>` | 35 | 11 | 0 |
| [Platform module](platform-module.md) | `/api/platform` (в api форка ICPlan) | UI — сессия администратора; Runner — сервисный токен | 0 | 0 | 10 |
| [Agent Runner ↔ Harness](agent-runner.md) | Harness: `http://<sandbox>:8090`; Runner: `http://agent-runner:8080` | одноразовый токен запуска `RUN_TOKEN` | 0 | 0 | 9 |
| [Memory API](memory.md) | `http://memory-api:8085` | токен запуска (Harness), сервисный токен (администрирование) | 0 | 0 | 4 |
| [LiteLLM gateway](llm-gateway.md) | `http://litellm:4000` | virtual key агента; админ — master key | 3 | 0 | 1 |
| [Guardrails (OPA)](guardrails.md) | `http://opa:8181` | внутренняя сеть (mTLS — этап 4) | 3 | 0 | 0 |
| [Sandbox](sandbox.md) | своего API нет: среду создаёт Runner | — | 3 | 0 | 0 |
| [Harness](harness.md) | см. Agent Runner ↔ Harness | токен запуска | 0 | 0 | 1 |
| [MCP / Tools](mcp-tools.md) | MCP-серверы по протоколу MCP (streamable HTTP) | ключ агента / секрет сервера | 2 | 0 | 0 |
| [Observability](observability.md) | в api ICPlan | сессия | 1 | 0 | 0 |
| [Инфраструктура](infrastructure.md) | ingress Traefik | TLS | 2 | 0 | 0 |

## Модели данных

Основные объекты, которыми обмениваются компоненты.

### Run

_выдача запуска (`/agent-runs/claim`)_

```json
{ "run": { "id": 1042, "agentId": 7, "issue": { "key": "MKT-42", "title": "…", "url": "…" },
          "trigger": "delegation", "prompt": "Work item MKT-42 has been delegated to you…",
          "rule": { "type": "process_step", "process": "Фича", "step": "SDD" } } }
```

### RunBundle

_Runner → Harness (`POST /run`)_

```json
{ "runId": 1042, "agent": { "model": "team-default", "version": 5, "instruction": "…", "skills": ["…"] },
  "guidance": "…", "params": { "model.temperature": 0.2, "limits.max_steps": 30 },
  "workspace": [ { "name": "repo", "type": "git", "url": "…", "branch": "agent/MKT-42", "right": "write" },
                 { "name": "task", "type": "folder", "prefix": "projects/MKT/tasks/42/", "right": "read" } ],
  "memory": { "m3": { … }, "m2": [ … ] }, "task": { "key": "MKT-42", "criteria": [ { "text": "…", "origin": "process" }, { "text": "…", "origin": "user:anna" }, { "text": "…", "origin": "agent:analyst" } ], "returnNote": null } }
```

### RunEvent

_шаг запуска (`/agent-runs/:id/events`, `/run/events`)_

```json
{ "runId": 1042, "seq": 7, "type": "tool_call", "at": "2026-10-10T12:00:05Z",
  "data": { "tool": "itsaplan_get_issue", "status": "ok", "ms": 220 } }
```

Соответствие OpenTelemetry GenAI (semconv v1.44.0, статус Development — имена атрибутов сверяются при экспорте; [R&D observability](../rnd/observability.md#e6)):

| `type` | Спан или событие OTel | Атрибуты |
|---|---|---|
| `run_started` / `run_finished` | спан `invoke_agent` (начало / конец) | агент, версия, `runId`; итог и токены — на конце |
| `llm_call` | спан `chat` (`gen_ai.operation.name`) | провайдер, модель запроса и ответа, токены ввода, вывода, размышлений |
| `tool_call` / `tool_result` | спан `execute_tool` | имя тула, статус, длительность |
| `memory_write` | спан `execute_tool` (тул памяти) | уровень памяти, область |
| `needs_approval`, `question`, `guardrail_decision` | событие спана `invoke_agent` | решение, точка G, причина |

### RunResult

_итог (`/agent-runs/:id/result`)_

```json
{ "status": "success", "output": "## Требования…", "artifacts": [ { "name": "requirements.md", "url": "s3://…" } ],
  "usage": { "prompt_tokens": 18450, "completion_tokens": 2210, "reasoning_tokens": 900, "cost_usd": 0.12, "steps": 9 } }
```

### ApprovalDecision

_решение пользователя; `scope`: `once` — только этот вызов, `run` — до конца запуска (R-GRD-03)_

```json
{ "runId": 1042, "seq": 8, "decision": "approve", "scope": "once", "by": "user:anna", "comment": null }
```

### UserMessage

_указание во время работы (ответ heartbeat)_

```json
{ "messages": [ { "id": "m-91", "text": "используй pytest", "by": "user:anna", "at": "…" } ] }
```

### Verdict

_вердикт по результату_

```json
{ "runId": 1042, "verdict": "rejected", "note": "нет тестов" }
```

### Process

_процесс типа задачи_

```json
{ "issueType": "Фича", "owner": "user:lead", "firstStep": "sdd",
  "steps": [ { "id": "sdd", "column": "SDD", "agent": "agent:analyst", "maxRuns": 3, "requireReview": false,
               "deliverable": "spec.md и tasks.md в ветке задачи",
               "doneCriteria": [ { "text": "у каждого требования есть сценарий", "origin": "process" } ],
               "criteriaApproval": "review",
               "onSuccess": { "step": "code" }, "onFailure": { "step": "help" } } ] }
```

### M3Record

_состояние задачи_

```json
{ "issue_key": "MKT-42", "scope": "issue", "agent": "analyst", "done": ["…"], "next": ["…"], "blockers": ["…"],
  "artifacts": [ { "path": "openspec/changes/mkt-42/spec.md", "ref": "agent/MKT-42@a1b2c3" } ],
  "questions": [ "…" ],
  "criteria_next": [ { "text": "тест на пустой список", "origin": "agent:analyst" } ] }
```

### PolicyInput / PolicyDecision

_OPA G1 / G2_

```json
{ "input": { "point": "g2", "agent": "dev", "tool": "git_push", "args_hash": "…", "autonomy": "R2" } }
{ "result": { "allow": false, "approval": true, "reason": "push требует подтверждения" } }
```

