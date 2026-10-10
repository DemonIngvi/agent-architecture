# Spec Delta

## Purpose

Контракт уровня C1: как ICPlan находит агентов, запускает задачи, подтверждает действия и получает события от Agent Platform.

## ADDED Requirements

### Requirement: Единый вход Integration API
Платформа SHALL предоставлять ICPlan единый Integration API в двух формах: REST и MCP-сервер с одинаковым набором операций. Внутренние компоненты (C2) MUST NOT быть доступны ICPlan напрямую.

#### Scenario: Одна операция в двух формах
- **WHEN** ICPlan вызывает `start_run` через REST или как MCP tool
- **THEN** результат одинаков

### Requirement: Каталог агентов
API SHALL предоставлять `list_agents` и `describe_agent`: возможности агента, схемы входа и выхода, цену и лимиты.

#### Scenario: Выбор агента
- **WHEN** ICPlan вызывает `describe_agent`
- **THEN** получает схему входа, схему выхода и лимиты агента

### Requirement: Запуски
API SHALL предоставлять `start_run` (по `agent_id` и `task_id`), `get_run`, `cancel_run`, `get_artifacts`.

#### Scenario: Запуск и результат
- **WHEN** ICPlan вызывает `start_run`, а затем `get_run` после завершения
- **THEN** получает статус `succeeded` и результат; файлы доступны через `get_artifacts`

### Requirement: Подтверждения и ответы
API SHALL предоставлять `approve_action` для подтверждения опасного действия агента (G2) и `answer_run` для ответа на вопрос агента.

#### Scenario: Подтверждение действия
- **WHEN** агент ждёт подтверждения и ICPlan вызывает `approve_action`
- **THEN** действие выполняется, запуск продолжается

### Requirement: События
Платформа SHALL отправлять ICPlan события `status`, `needs_approval`, `question`, `done` через webhook или очередь, без необходимости опроса.

#### Scenario: Нужен ответ
- **WHEN** агенту требуется подтверждение
- **THEN** ICPlan получает событие `needs_approval` с `run_id` и описанием действия

### Requirement: Аутентификация и квоты
Каждый вызов API MUST быть аутентифицирован; платформа SHALL применять квоты на клиента.

#### Scenario: Превышение квоты
- **WHEN** ICPlan превысил квоту запусков
- **THEN** вызов отклоняется с ошибкой квоты

### Requirement: Идемпотентность
`start_run` MUST быть идемпотентным по ключу идемпотентности.

#### Scenario: Повторная отправка
- **WHEN** ICPlan повторно отправляет `start_run` с тем же ключом
- **THEN** возвращается тот же `run_id`, второй запуск не создаётся

### Requirement: Версионирование API
API SHALL иметь явную версию; несовместимые изменения MUST выпускаться только в новой версии.

#### Scenario: Старый клиент
- **WHEN** выходит новая версия API
- **THEN** клиент на прежней версии продолжает работать
