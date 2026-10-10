"""Hook MkDocs для локального просмотра: перед каждой сборкой заново копирует исходные .md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402


def on_pre_build(config, **kwargs):
    build.copy_sources()
