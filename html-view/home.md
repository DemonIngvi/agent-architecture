<h1 class="home-title">Agent Platform</h1>

<div class="map">

  <div class="actors">
    <span class="actor">👤 Пользователь ICPlan</span>
    <span class="actor">🛠 Администратор</span>
  </div>
  <div class="flow">↓ задачи, доска, процесс · настройка агентов ↓</div>

  <div class="zone zone-icplan">
    <div class="zone-title"><a href="components/icplan/">ICPlan</a> <span>It's a Plan · таск-трекер · уже есть, дорабатываем</span></div>
    <div class="grid4">
      <a class="card" href="components/icplan/">
        <i class="st st-done"></i><b>Control Plane UI</b>
        <small>Настройка агентов: модель, инструкция, тулы, навыки, MCP</small>
      </a>
      <a class="card" href="components/icplan/">
        <i class="st st-part"></i><b>Registry</b>
        <small>Агенты, тулы, навыки, ключи. Нужны версии и экспорт YAML</small>
      </a>
      <a class="card" href="components/icplan/">
        <i class="st st-part"></i><b>Run Queue</b>
        <small>Очередь запусков и протокол внешнего раннера</small>
      </a>
      <a class="card" href="components/icplan/">
        <i class="st st-part"></i><b>Task UI</b>
        <small>Доска, процесс задачи (D17), чат запуска с вопросами и подтверждениями (D21)</small>
      </a>
    </div>
  </div>

  <div class="flow">↓ агент, задача из очереди &nbsp;·&nbsp; стрим и результат ↑</div>

  <div class="row3">
    <a class="card card-side" href="components/platform-module/">
      <i class="st st-todo"></i><b>Platform module</b>
      <small>Модуль ICPlan: автономия, бюджеты, профили среды и памяти, доступы, данные guardrails</small>
    </a>
    <a class="card card-main" href="components/agent-runner/">
      <i class="st st-todo"></i><b>Agent Runner</b> <span class="g">G1</span>
      <small>Берёт запуск из очереди ICPlan, выдаёт sandbox из тёплого пула, следит за лимитами, возвращает итог</small>
    </a>
    <div></div>
  </div>

  <div class="flow">↓ claim из тёплого пула · run · destroy</div>

  <div class="row3">
    <a class="card card-side card-guard" href="components/guardrails/">
      <i class="st st-todo"></i><b>Guardrails</b>
      <small>Rego в git + данные в БД. Каждая точка включается в конфиге деплоя</small>
      <span class="chips"><span class="g">G1</span><span class="g">G2</span><span class="g">G3</span><span class="g">G4</span> OPA</span>
    </a>

    <div class="zone zone-sandbox">
      <div class="zone-title"><a href="components/sandbox/">Sandbox</a> <span class="g">G3</span> <span>одноразовый контейнер · /workspace</span></div>
      <a class="card card-harness" href="components/harness/">
        <i class="st st-todo"></i><b>Harness</b> <span class="g">G2</span>
        <small>Агентский цикл на LangGraph: пауза на approve, возобновление, стрим шагов</small>
        <span class="chips"><span class="chip">Context Mgr</span><span class="chip">LLM client</span><span class="chip">Tool Exec</span><span class="chip">hooks</span><span class="chip">M0</span></span>
      </a>
    </div>

    <div class="stack">
      <a class="card" href="components/memory/">
        <i class="st st-part"></i><b>Memory</b>
        <small>M1 M2 M5 M6 есть · M3 первым · M4 с RAG</small>
      </a>
      <a class="card" href="components/mcp-tools/">
        <i class="st st-part"></i><b>MCP / Tools</b>
        <small><code>itsaplan-core</code> есть · git-провайдер · правила R1–R7</small>
      </a>
    </div>
  </div>

  <div class="flow">↓ prompt · ответ ↑</div>

  <div class="row3">
    <div></div>
    <a class="card card-main" href="components/llm-gateway/">
      <i class="st st-part"></i><b>LiteLLM gateway</b> <span class="g">G4</span>
      <small>Единственный выход к моделям: алиасы, virtual key на агента, лимиты, fallback. Развёрнут, не подключён</small>
    </a>
    <a class="card" href="components/observability/">
      <i class="st st-part"></i><b>Observability</b>
      <small>События запуска (AG-UI) → чат запуска в задаче, затраты</small>
    </a>
  </div>

  <div class="flow">↓</div>
  <div class="providers">
    <span class="chip">mock-LLM (разработка)</span><span class="chip">Anthropic</span><span class="chip">OpenAI</span><span class="chip">локальные модели</span>
  </div>

</div>

<div class="hero hero-below">
  <p>Платформа запуска LLM-агентов для задач таск-трекера ICPlan: изоляция каждого запуска, контроль моделей и затрат, guardrails, память.</p>
</div>

<div class="why-platform">
  <h2>Зачем платформа</h2>
  <p>В ICPlan агенты уже есть, но исполняются внутри трекера или CLI на машине оператора. Платформа добавляет то, чего не хватает для работы агентов в процессе:</p>
  <table>
    <thead><tr><th>Проблема без платформы</th><th>Что даёт платформа</th><th>Компонент</th></tr></thead>
    <tbody>
      <tr><td>Агент исполняется без изоляции, рядом с данными трекера</td><td>Каждый запуск — в своём одноразовом контейнере</td><td><a href="components/sandbox/">Sandbox</a>, <a href="components/agent-runner/">Agent Runner</a></td></tr>
      <tr><td>Модели вызываются напрямую, затраты не видны</td><td>Одна точка выхода к моделям, бюджеты, учёт по задаче, смена модели без кода</td><td><a href="components/llm-gateway/">LiteLLM gateway</a></td></tr>
      <tr><td>Нет правил, что агенту можно</td><td>Политики в 4 точках, approve опасных действий, аудит</td><td><a href="components/guardrails/">Guardrails</a></td></tr>
      <tr><td>Следующий агент не знает, что сделал предыдущий</td><td>Память задачи и истории запусков</td><td><a href="components/memory/">Memory</a></td></tr>
      <tr><td>Задачу нужно вручную отдавать агенту</td><td>Автоподхват по статусу и типу задачи</td><td><a href="components/icplan/">ICPlan</a></td></tr>
      <tr><td>Видно только итог работы агента</td><td>Чат запуска и затраты в задаче</td><td><a href="components/observability/">Observability</a></td></tr>
      <tr><td>Настройки агента ограничены моделью и инструкцией</td><td>Бюджеты, профили среды и памяти, правила, версии</td><td><a href="components/platform-module/">Platform module</a></td></tr>
    </tbody>
  </table>
</div>

<div class="legend">
  <span><i class="st st-done"></i>есть</span>
  <span><i class="st st-part"></i>частично</span>
  <span><i class="st st-todo"></i>не начато</span>
  <span><b class="g">G1–G4</b> точки guardrails</span>
  <span>Клик по блоку — описание и устройство компонента; спеки и задачи — рядом на его странице</span>
</div>
