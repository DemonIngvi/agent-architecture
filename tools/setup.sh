#!/usr/bin/env sh
# Подготовка репозитория для любого агента и человека: git-хуки проекта и проверка Python.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit tools/doc 2>/dev/null
"$ROOT/tools/doc" check >/dev/null 2>&1 && echo "ok: проверки документации работают" || echo "внимание: ./tools/doc check сообщает замечания или Python не найден"
echo "git-хуки: $(git config core.hooksPath)"
