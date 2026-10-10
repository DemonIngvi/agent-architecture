# Типы документов и правила

← [Правила документации](README.md)

Общие правила для всех: русский язык; заголовки OpenSpec и SHALL/MUST — на английском; в начале файла строка «←» на родителя; все упоминания документов — ссылками; схемы — ASCII по [FORMAT.md](../../FORMAT.md); секретов нет.

| Тип | Где | Обязательные разделы | Правила | Синхронизировать |
|---|---|---|---|---|
| **Корень** | `README.md` | что за платформа, ссылки на разделы, таблица компонентов | компонент = строка таблицы с готовностью | architecture.md, html-view/components.py |
| **Архитектура** | `architecture.md` | C1, C2, разделы решений, блоки, доработки | меняем только по необходимости; у раздела решения — «Обоснование» со ссылкой на R&D и design | design, спеки, страницы компонентов |
| **Формат схем** | `FORMAT.md` | правила ASCII-схем | — | — |
| **Потоки** | `docs/flows/<компонент>.md`, `README.md` | таблица потоков (от → к, данные), примеры данных | данные — черновик контракта до фиксации в задаче | спека (сценарии), design, IO в components.py |
| **R&D** | `docs/rnd/<тема>.md` | по [методологии](../rnd/METHOD.md): итог сверху, контекст, knock-out, критерии, матрица, профиль, последствия, источники | данные репозиториев — из GitHub API с датой; не подгонять баллы | design (D-номер), REFS в rationale.py, «Обоснование» в architecture.md и спеке |
| **Задача** | `docs/tasks/<N.M>-<slug>.md` | таблица оценок, Зачем, Что сделать, Приёмка, Как прокликать, INVEST, Декомпозиция (2–8 ч), Что проработать | ссылается на требование спеки; выполненное — `[x]` | ROADMAP, TASKS, tasks.md change, components.py (tids) |
| **Roadmap** | `docs/ROADMAP.md` | этапы, таблицы задач, итоги | итоги пересчитываются при добавлении задачи | задачи |
| **Сводная таблица** | `docs/TASKS.md` | по компонентам: сделано → нужно | ссылки на документы задач | задачи |
| **Бэклог** | `docs/BACKLOG.md` | что отложено и почему | — | architecture.md |
| **Proposal** | `openspec/changes/<change>/proposal.md` | Why, What Changes, Capabilities, Impact | capability названа по поведению, не по работе | specs |
| **Spec** | `openspec/changes/<change>/specs/<cap>/spec.md` | Purpose, Requirements, Scenarios | [критерии полноты](spec-criteria.md) | architecture.md, flows, задачи |
| **Схема capability** | `.../specs/<cap>/architecture.md` | схема, блоки, расширения, плюсы / минусы по модулям | только схема, без требований | spec.md |
| **Design** | `openspec/changes/<change>/design.md` | Context, Goals, Decisions (D-номера), Risks, Open Questions | у решения — альтернативы и ссылка на R&D | R&D, architecture.md |
| **Tasks change** | `openspec/changes/<change>/tasks.md` | `## N.` группы, `- [ ] N.M` | одна строка + ссылка на docs/tasks | docs/tasks |
| **Данные сайта** | `html-view/components.py`, `rationale.py`, `subcomponents.py`, `home.md` | COMPONENTS, BLOCKS, ABOUT, IO, RATIONALE, REFS, SUB | меняются вместе с архитектурой; новый блок схемы с описанием — в SUB | architecture.md, R&D, задачи |
| **Правила** | `docs/rules/` | этот раздел | при новом типе документа — добавить строку сюда | — |
