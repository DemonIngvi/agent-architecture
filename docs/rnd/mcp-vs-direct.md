# R&D: MCP или прямой вызов

← [Все R&D](README.md) · компонент: MCP / Tools · решение: [design D10](../../openspec/changes/define-agent-platform/design.md)

## Что говорит индустрия

- Если последовательность известна заранее — прямой API; если следующий шаг решает модель — MCP / тул.
- MCP выигрывает при переиспользовании интеграций между хостами и когда секреты должны оставаться вне агента.
- Прямые вызовы эффективнее по токенам и в разы быстрее в пакетных операциях.

## Правила

| # | Правило | Как |
|---|---|---|
| R1 | Последовательность известна заранее | Прямой вызов |
| R2 | Следующий шаг решает модель | Тул агента |
| R3 | Тул нужен нескольким агентам или держит секрет | MCP-сервер |
| R4 | Тул один, стабильный, только внутри Harness | Нативный тул |
| R5 | Пакетные операции | Прямой вызов |
| R6 | Админ-функции | Отдельные MCP по уровню доверия |
| R7 | Внутренности платформы | Только прямой вызов |

## Решение

Гибрид R1–R7. Требование проекта AI-агент «всё через MCP» смягчено до R6 (админ-MCP — в бэклоге).

## Источники

- [MCP vs API architecture patterns — PromptLayer](https://blog.promptlayer.com/mcp-vs-api-architecture-patterns-for-ai-agents-and-applications/)
- [MCP vs API for AI agents — Nylas](https://cli.nylas.com/guides/mcp-vs-api-ai-agents)
- [MCP vs Function Calling in Agents 2026](https://www.kunalganglani.com/blog/mcp-vs-function-calling-agents.md)
- [Building agents that reach production systems with MCP — Claude](https://claude.com/es/resources/articles/building-agents-that-reach-production-systems-with-mcp)
- Проект AI-агент: `platform/technical/layers-and-mcp.md` §2
