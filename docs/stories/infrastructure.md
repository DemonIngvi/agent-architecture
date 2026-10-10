# User Stories: Инфраструктура

← [Все истории](README.md) · [потоки](../flows/infrastructure.md)

> Сгенерировано из `html-view/stories.py` — правьте там.

## Процесс (BPMN)

<!-- bpmn:infrastructure -->

| Шаг | Дорожка | Тип | Переходы |
|---|---|---|---|
| Новая версия | Эксплуатация | начало | → helm upgrade |
| helm upgrade | k3s / Helm | задача | → Миграции нужны? |
| Миграции нужны? | k3s / Helm | развилка | да → Миграции БД; нет → Реплики по одной |
| Миграции БД | Данные | задача | → Реплики по одной |
| Реплики по одной | k3s / Helm | задача | → Readiness ок? |
| Readiness ок? | k3s / Helm | развилка | да → Версия выпущена; нет → Откат ревизии |
| Откат ревизии | k3s / Helm | задача | → Разбор инцидента |
| Разбор инцидента | Эксплуатация | ошибка | — |
| Версия выпущена | Эксплуатация | конец | — |

## Истории

### US-INF-01

**Как** эксплуатация, **я хочу** развернуть платформу на чистом сервере одной командой, **чтобы** установка была воспроизводимой.

**Критерии приёмки:**

- [ ] Скрипт ставит k3s, namespaces, чарты
- [ ] Повторный запуск не пересоздаёт данные
- [ ] Нет обязательного Secret → понятная ошибка

**Требования:** [Кластер Kubernetes](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) · [Упаковка и развёртывание Helm](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) · [Секреты](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md)

### US-INF-02

**Как** пользователь icplan, **я хочу** открывать ICPlan по HTTPS, **чтобы** работать безопасно.

**Критерии приёмки:**

- [ ] HTTP → перенаправление на HTTPS
- [ ] Админки снаружи недоступны

**Требования:** [Ingress и TLS](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md)

### US-INF-03

**Как** эксплуатация, **я хочу** чтобы платформа выдерживала пиковую нагрузку команды, **чтобы** агенты и люди не мешали друг другу.

**Критерии приёмки:**

- [ ] Пик профиля → p95 < 300 мс
- [ ] Превышение → очередь, а не падение узла
- [ ] Замер обновляет профиль

**Требования:** [Профиль нагрузки и ёмкость](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) · [Балансировка между репликами](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md)

### US-INF-04

**Как** эксплуатация, **я хочу** восстановить данные после потери сервера, **чтобы** не потерять работу команды.

**Критерии приёмки:**

- [ ] Копии вне узла
- [ ] Ежемесячная проверка восстановления
- [ ] Нет копии → предупреждение

**Требования:** [Резервное копирование](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) · [СУБД и пул соединений](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md)

### US-INF-05

**Как** эксплуатация, **я хочу** обновлять компоненты без простоя, **чтобы** не прерывать работу агентов.

**Критерии приёмки:**

- [ ] Замена реплик по одной
- [ ] Откат при провале проверок

**Требования:** [Упаковка и развёртывание Helm](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md) · [Проверки готовности и порядок запуска](../../openspec/changes/define-agent-platform/specs/platform-infrastructure/spec.md)

