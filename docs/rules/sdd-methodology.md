# Методология SDD-требований

← [Правила документации](README.md) · [критерии полноты спеки](spec-criteria.md)

Spec-Driven Development (SDD): спецификация, а не код — источник правды; агент реализует по спеке. Мы опираемся на три популярные практики и связываем их с нашими артефактами.

## Практики

| Практика | Что берём | Где у нас |
|---|---|---|
| **OpenSpec** | формат дельт, Requirement / Scenario, SHALL / MUST, WHEN / THEN, `validate --strict` | `openspec/changes/*/specs/*/spec.md` |
| **GitHub Spec Kit** (1.0, 2026) | цепочка: **constitution** (принципы проекта) → **specify** (истории и критерии приёмки) → **plan** (архитектура, данные) → **tasks** (упорядоченные задачи) | constitution — `docs/rules/` + `openspec/config.yaml`; specify — `docs/stories/` + `spec.md`; plan — `design.md`, `architecture.md`, `interfaces.md`; tasks — `docs/tasks/`, `tasks.md` |
| **EARS** — Easy Approach to Requirements Syntax (Rolls-Royce; используется в AWS Kiro) | 5 шаблонов текста требования — однозначность и проверяемость | текст `### Requirement` |

## Шаблоны EARS для текста требования

| Тип | Шаблон | Пример |
|---|---|---|
| Всегда (ubiquitous) | Система SHALL … | Harness SHALL вызывать модели только через LLM Gateway |
| Событие (event-driven) | WHEN <событие>, система SHALL … | WHEN задача вошла в статус с агентом, ICPlan SHALL поставить запуск в очередь |
| Состояние (state-driven) | WHILE <состояние>, система SHALL … | WHILE запуск ждёт подтверждения, Runner SHALL держать слот задачи |
| Опция (optional) | WHERE <включена функция>, система SHALL … | WHERE включён G2, Harness SHALL проверять каждый вызов тула |
| Нежелательное поведение (unwanted) | IF <сбой / ошибка>, THEN система SHALL … | IF OPA недоступен, THEN Harness SHALL отклонить действие |

Правила:

- Одно требование — один шаблон и одно поведение (ISO/IEC/IEEE 29148, «единичное»).
- Отказы и ошибки — только шаблоном **IF … THEN** (связь с FMEA).
- Переключатели конфигурации — шаблоном **WHERE**.
- Сценарии остаются в формате OpenSpec WHEN / THEN.

## Порядок работы (наш SDD-цикл)

```
constitution ─▶ specify ──────────────▶ plan ───────────────────────▶ tasks ─────────▶ реализация
docs/rules       User Stories + BPMN     R&D → design → architecture   docs/tasks (INVEST)   агент по спеке
openspec/config  → spec.md (EARS)        → interfaces.md (L0–L3, S, I,  → RTM (трассировка)
                 → критерии приёмки        FMEA, нагрузка, развёртывание)
```

## Источники

- [GitHub Spec Kit, обзор SDD 2026](https://codemyspec.com/blog/spec-driven-development)
- [Spec-Driven Development: the definitive 2026 guide](https://www.thebcms.com/blog/spec-driven-development/)
- [Kiro — feature specs (EARS)](https://kiro.dev/docs/specs/feature-specs/)
- [Kiro spec process methodology](https://github.com/jasonkneen/kiro/blob/main/spec-process-guide/methodology/overview.md)
- [Spec-Driven Development, without the hype](https://utsabpant.com/blog/spec-driven-development-without-the-hype)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
