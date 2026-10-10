# R&D: СУБД и хранилища

← [Все R&D](README.md) · [методология](../rules/rnd-methodology.md) · компонент: **Инфраструктура** · решение: [design D4, D15](../../openspec/changes/define-agent-platform/design.md)

## Итог

| | |
|---|---|
| **Решение** | PostgreSQL 17 + pgvector под CloudNativePG (пулер PgBouncer, бэкап в S3); объектное хранилище — RustFS (S3 API) |
| **Версия** | PostgreSQL 17; CloudNativePG v1.30.1; RustFS 1.0.x |
| **Лицензия** | PostgreSQL; Apache-2.0; Apache-2.0 |
| **Стоимость** | 0 $ |
| **Ключевые параметры** | одна БД-инстанция: БД `itsaplan` (схемы `public`, `platform`, `harness_ckpt`) и БД `litellm`; бэкап — базовые копии + WAL в S3 вне узла |
| **Статус** | Adopt (Postgres, RustFS), Trial (CloudNativePG) |
| **Оценка** | CloudNativePG + RustFS: **90** · CloudNativePG + SeaweedFS: **88** · ~~MinIO: 83~~ ✗ · Postgres StatefulSet (чарт ICPlan) + RustFS: **82** |

## Контекст

Платформе нужны: реляционная БД (ICPlan, наши схемы, LiteLLM, checkpoint), векторный поиск позже (M4), объектное хранилище (вложения, артефакты, бэкапы). ICPlan уже использует `pgvector/pgvector:pg17` и `rustfs/rustfs:1.0.0`.

## Обязательные требования (knock-out)

- Проект активно поддерживается

- ✗ **MinIO** — репозиторий архивирован, последний релиз 2025-10

## Критерии и веса

| Ф Функц. | П Произв. | Н Надёжн. | Б Безоп. | И Интегр. | Л Лиц./цена | З Зрелость | Р Распростр. | Э Эксплуат. |
|---|---|---|---|---|---|---|---|---|
| 20 | 10 | 10 | 10 | 10 | 10 | 10 | 5 | 5 |

## Матрица оценки

Оценка 1–5; итог = Σ(вес × оценка) / 5, максимум 100.

| Вариант | Ф | П | Н | Б | И | Л | З | Р | Э | **Итог** |
|---|---|---|---|---|---|---|---|---|---|---|
| Postgres StatefulSet (чарт ICPlan) + RustFS | 4 | 4 | 3 | 4 | 5 | 5 | 4 | 4 | 4 | **82** |
| CloudNativePG + RustFS | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 3 | **90** |
| CloudNativePG + SeaweedFS | 5 | 4 | 5 | 4 | 3 | 5 | 5 | 4 | 3 | **88** |
| MinIO ✗ | 5 | 5 | 5 | 4 | 5 | 3 | 1 | 5 | 4 | **83** |

## Профиль технологий

Данные GitHub API на 10.10.2026.

| Технология | Лицензия | ★ | Последний релиз | Активность | Распространённость, поток, токены, сеть |
|---|---|---|---|---|---|
| PostgreSQL 17 | PostgreSQL License | 22 329 | 17.x | 10.10.2026 | основная БД; образ `pgvector/pgvector:pg17` уже в стеке |
| pgvector | PostgreSQL License | 23 298 | — | 08.10.2026 | векторы для M4 / RAG |
| CloudNativePG | Apache-2.0 | 9 422 | v1.30.1 | 10.10.2026 | CNCF; оператор Postgres: реплики, пулер PgBouncer, бэкап в S3 (Barman) |
| RustFS | Apache-2.0 | 34 680 | 1.0.1 | 10.10.2026 | S3-совместимое хранилище; уже в стеке ICPlan |
| SeaweedFS | Apache-2.0 | 35 375 | 4.48 | 10.10.2026 | S3-совместимое, зрелое; запасной вариант |
| MinIO | AGPL-3.0 | 61 330 | 2025-10-15 | 24.04.2026 | **архивирован** — исключён |

Разница CloudNativePG и StatefulSet (88 против 81) — за счёт бэкапов, пулера и восстановления из коробки. Для этапов 1–2 остаётся compose с теми же образами.

## Последствия

**Плюсы**

- Одна СУБД на всё — проще эксплуатация
- Бэкап вне узла закрывает риск X5 из ревью

**Минусы и риски**

- Один инстанс Postgres — общая точка отказа ICPlan, платформы и LiteLLM
- RustFS молод (1.0) — нужен план миграции на SeaweedFS при проблемах

## Источники

- [PostgreSQL](https://github.com/postgres/postgres)
- [pgvector](https://github.com/pgvector/pgvector)
- [CloudNativePG](https://github.com/cloudnative-pg/cloudnative-pg)
- [RustFS](https://github.com/rustfs/rustfs)
- [SeaweedFS](https://github.com/seaweedfs/seaweedfs)
- [MinIO (архив)](https://github.com/minio/minio)
- Методология: [методология R&D](../rules/rnd-methodology.md)
