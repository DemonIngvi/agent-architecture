---
hide:
  - navigation
  - toc
---

<div class="hero">
  <h1>Agent Platform</h1>
  <p>Платформа запуска LLM-агентов для задач таск-трекера ICPlan: изоляция каждого запуска, контроль моделей и затрат, guardrails, память.</p>
  <div class="hero-actions">
    <a class="md-button md-button--primary" href="docs/ROADMAP/">Roadmap MVP</a>
    <a class="md-button" href="docs/TASKS/">Задачи</a>
    <a class="md-button" href="architecture/">Схемы C1 / C2</a>
    <a class="md-button" href="docs/HOW-TO-READ/">Как читать</a>
  </div>
</div>

<div class="legend">
  <span><i class="st st-done"></i>есть</span>
  <span><i class="st st-part"></i>частично</span>
  <span><i class="st st-todo"></i>не начато</span>
  <span><b class="g">G1–G4</b> точки guardrails</span>
  <span>Клик по блоку — описание и спека</span>
</div>

<div class="map">

  <div class="actors">
    <span class="actor">👤 Пользователь ICPlan</span>
    <span class="actor">🛠 Администратор</span>
  </div>
  <div class="flow">↓ задачи, доска, процесс · настройка агентов ↓</div>

  <div class="zone zone-icplan">
    <div class="zone-title">ICPlan <span>It's a Plan · таск-трекер · уже есть, дорабатываем</span></div>
    <div class="grid4">
      <a class="card" href="openspec/changes/define-agent-platform/specs/control-plane/spec/">
        <i class="st st-done"></i><b>Control Plane UI</b>
        <small>Настройка агентов: модель, инструкция, тулы, навыки, MCP</small>
      </a>
      <a class="card" href="openspec/changes/define-agent-platform/specs/agent-registry/spec/">
        <i class="st st-part"></i><b>Registry</b>
        <small>Агенты, тулы, навыки, ключи. Нужны версии и экспорт YAML</small>
      </a>
      <a class="card" href="openspec/changes/add-icplan-integration/specs/icplan-integration/spec/">
        <i class="st st-part"></i><b>Run Queue</b>
        <small>Очередь запусков и протокол внешнего раннера</small>
      </a>
      <a class="card" href="openspec/changes/icplan-agent-autopickup/specs/icplan-agent-autopickup/architecture/">
        <i class="st st-part"></i><b>Task UI</b>
        <small>Доска, чат, approve, таймлайн. Нужен автоподхват задач агентом</small>
      </a>
    </div>
  </div>

  <div class="flow">↓ агент, задача из очереди &nbsp;·&nbsp; стрим и результат ↑</div>

  <div class="row3">
    <a class="card card-side" href="openspec/changes/define-agent-platform/specs/control-plane/spec/">
      <i class="st st-todo"></i><b>Platform module</b>
      <small>Модуль ICPlan: алиасы LLM, бюджеты, профили sandbox и памяти, данные guardrails</small>
    </a>
    <a class="card card-main" href="openspec/changes/define-agent-platform/specs/agent-runner/spec/">
      <i class="st st-todo"></i><b>Agent Runner</b> <span class="g">G1</span>
      <small>Берёт запуск из очереди ICPlan, выдаёт sandbox из тёплого пула, следит за лимитами, возвращает итог</small>
    </a>
    <div></div>
  </div>

  <div class="flow">↓ claim из тёплого пула · run · destroy</div>

  <div class="row3">
    <a class="card card-side card-guard" href="openspec/changes/define-agent-platform/specs/guardrails/spec/">
      <i class="st st-todo"></i><b>Guardrails</b>
      <small>Rego в git + данные в БД. Каждая точка включается в конфиге деплоя</small>
      <span class="chips"><span class="g">G1</span><span class="g">G2</span><span class="g">G3</span><span class="g">G4</span> OPA</span>
    </a>

    <div class="zone zone-sandbox">
      <div class="zone-title"><a href="openspec/changes/define-agent-platform/specs/agent-sandbox/spec/">Sandbox</a> <span class="g">G3</span> <span>одноразовый контейнер · /workspace</span></div>
      <a class="card card-harness" href="openspec/changes/define-agent-platform/specs/agent-harness/spec/">
        <i class="st st-todo"></i><b>Harness</b> <span class="g">G2</span>
        <small>Агентский цикл на LangGraph: пауза на approve, возобновление, стрим шагов</small>
        <span class="chips"><span class="chip">Context Mgr</span><span class="chip">LLM client</span><span class="chip">Tool Exec</span><span class="chip">hooks</span><span class="chip">M0</span></span>
      </a>
    </div>

    <div class="stack">
      <a class="card" href="openspec/changes/define-agent-platform/specs/agent-memory/spec/">
        <i class="st st-part"></i><b>Memory</b>
        <small>M1 M2 M5 M6 есть · M3 первым · M4 с RAG</small>
      </a>
      <a class="card" href="openspec/changes/define-agent-platform/specs/tool-integration/spec/">
        <i class="st st-part"></i><b>MCP / Tools</b>
        <small><code>itsaplan-core</code> есть · git-провайдер · правила R1–R7</small>
      </a>
    </div>
  </div>

  <div class="flow">↓ prompt · ответ ↑</div>

  <div class="row3">
    <div></div>
    <a class="card card-main" href="openspec/changes/define-agent-platform/specs/llm-gateway/spec/">
      <i class="st st-part"></i><b>LiteLLM gateway</b> <span class="g">G4</span>
      <small>Единственный выход к моделям: алиасы, virtual key на агента, лимиты, fallback. Развёрнут, не подключён</small>
    </a>
    <a class="card" href="openspec/changes/define-agent-platform/specs/observability/spec/">
      <i class="st st-part"></i><b>Observability</b>
      <small>События запуска → таймлайн в задаче, затраты</small>
    </a>
  </div>

  <div class="flow">↓</div>
  <div class="providers">
    <span class="chip">mock-LLM (разработка)</span><span class="chip">Anthropic</span><span class="chip">OpenAI</span><span class="chip">локальные модели</span>
  </div>

</div>

<div class="links3">
  <a class="card" href="docs/ROADMAP/"><b>🗺 Roadmap MVP</b><small>4 этапа, 23 задачи, оценки по времени и токенам</small></a>
  <a class="card" href="docs/tasks/1.1-mock-llm-litellm/"><b>▶ Первая задача</b><small>1.1 Mock-LLM и LiteLLM</small></a>
  <a class="card" href="overview/"><b>📋 Компоненты</b><small>Таблица компонентов, интеграции, готовность</small></a>
  <a class="card" href="openspec/changes/define-agent-platform/design/"><b>⚖ Решения</b><small>Design D1–D13: почему так</small></a>
  <a class="card" href="docs/BACKLOG/"><b>🗄 Бэклог</b><small>Что отложено и почему</small></a>
  <a class="card" href="https://github.com/DemonIngvi/agent-architecture"><b>⌥ GitHub</b><small>Исходники документации</small></a>
</div>
