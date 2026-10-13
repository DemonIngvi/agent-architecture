"""Интеграции, контракты и модель данных компонентов — единый источник для карточек и страницы «Модель данных».

Данные — YAML по единице в data/ (yamldata.py; правило: docs/rules/data-methodology.md#yaml); здесь только загрузка, имена прежние.
- интерфейсы I-коды → data/integrations.yaml (INTEG, INTEG_TYPES, ALSO, DATA_IN_RESPONSE);
- модели обмена → data/models/<Имя>.yaml (MODELS, MODEL_META = source, FIELD_SRC, PLANNED); NAMING → data/datamodel.yaml;
- эндпоинты вне OpenAPI форка и доработки форка → data/endpoints/<страница API>.yaml (ENDPOINT_IO);
- таблицы → data/tables/<имя>.yaml: платформы (PLATFORM_TABLES, SCHEMA_OF), форка (FORK_COLUMNS, FORK_WRITTEN), LiteLLM (LITELLM_TABLES),
  политика хранения (TABLE_POLICY); ICPLAN_TABLES и STORES — в data/components/<slug>.yaml;
- базы данных → data/databases.yaml (DB_CLUSTER, DATABASES, DB_GRANTS, MIGRATE); S1_DOMAINS, TREES, LITELLM_REF → data/datamodel.yaml.
Источники фактов: матрица docs/data-types.md и interfaces.md спек; таблицы ICPlan — код форка (icplan_schema.json,
python html-view/schema_import.py); таблицы платформы — проект схемы по спекам и решениям D4, D17–D20; LiteLLM — schema.prisma v1.104.2.
Правило: docs/rules/change-process.md (новый интерфейс, хранилище или модель → единица в data/).
"""
import yamldata as _Y

_D = _Y.datamodel()
INTEG = _D["INTEG"]
INTEG_TYPES = _D["INTEG_TYPES"]
DATA_IN_RESPONSE = _D["DATA_IN_RESPONSE"]
ALSO = _D["ALSO"]
MODELS = _D["MODELS"]
NAMING = _D["NAMING"]
MODEL_META = _D["MODEL_META"]
FIELD_SRC = _D["FIELD_SRC"]
PLANNED = _D["PLANNED"]
ICPLAN_TABLES = _D["ICPLAN_TABLES"]
PLATFORM_TABLES = _D["PLATFORM_TABLES"]
LITELLM_REF = _D["LITELLM_REF"]
LITELLM_TABLES = _D["LITELLM_TABLES"]
S1_DOMAINS = _D["S1_DOMAINS"]
DB_CLUSTER = _D["DB_CLUSTER"]
DATABASES = _D["DATABASES"]
DB_GRANTS = _D["DB_GRANTS"]
SCHEMA_OF = _D["SCHEMA_OF"]
MIGRATE = _D["MIGRATE"]
FORK_WRITTEN = _D["FORK_WRITTEN"]
TABLE_POLICY = _D["TABLE_POLICY"]
STORES = _D["STORES"]
TREES = _D["TREES"]
ENDPOINT_IO = _D["ENDPOINT_IO"]
FORK_COLUMNS = _D["FORK_COLUMNS"]
