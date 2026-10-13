"""User Stories и процессы (BPMN-нотация) по компонентам.

Данные — YAML по единице (yamldata.py; правило: docs/rules/data-methodology.md#yaml), здесь только загрузка, имена прежние:
- data/stories/<компонент>/<US-ID>.yaml — история: STORIES[slug] = [(id, роль, хочу, чтобы, [критерии приёмки], [требования спеки], точка входа)];
  поле chain — сквозная трассировка CHAINS[история] = ([истории по порядку], конечная точка); порядок — _order.yaml папки;
- data/processes/<компонент>.yaml — BPMN[slug] = [dict(title, stories, lanes, steps, artifacts)],
  steps = [(id, дорожка, тип, подпись, [(куда, подпись стрелки)])], типы шагов: start, task, gateway, end, error;
  ARTIFACTS[slug] — артефакты первого процесса (или поле artifacts файла);
- data/personas.yaml — ROLES и PERSONAS (id → (имя, что может, что хочет, конфликт, промпт для отыгрыша)).
Методика: docs/rules/us-methodology.md
"""
import yamldata as _Y

_D = _Y.stories()
ROLES = _D["ROLES"]
STORIES = _D["STORIES"]
BPMN = _D["BPMN"]
PERSONAS = _D["PERSONAS"]
ARTIFACTS = _D["ARTIFACTS"]
CHAINS = _D["CHAINS"]
