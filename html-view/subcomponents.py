"""Подкомпоненты (внутренние блоки схем): технология, ключевые параметры, что делает, почему так.

Данные — data/blocks/<компонент>/<slug>.yaml, по файлу на блок (yamldata.py; правило: docs/rules/data-methodology.md#yaml);
порядок блоков компонента — data/blocks/<компонент>/_order.yaml. Здесь только загрузка, имя прежнее.
Ключ SUB — (slug компонента, название блока на схеме = поле title). Блок с описанием становится ссылкой.
Поля: tech, kind, stories, screens, params [(параметр, значение)], does [..], io, data, reqs, tasks, failures, why, rnd (файл в docs/rnd или ""),
ops, schema, iface — схема и допустимые значения: yamldata.SCHEMAS["block"], проверка: python html-view/doctool.py yaml-check.
"""
import yamldata as _Y

SUB = _Y.sub()
