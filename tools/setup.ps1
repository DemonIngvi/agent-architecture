# Подготовка репозитория (Windows): git-хуки проекта и проверка Python.
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
git config core.hooksPath .githooks
& "$Root\tools\doc.cmd" yaml-schema | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Output "ok: JSON Schema редактора для data/*.yaml (.vscode/settings.json → yaml.schemas)" }
& "$Root\tools\doc.cmd" check | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Output "ok: проверки документации работают" } else { Write-Output "внимание: tools\doc.cmd check сообщает замечания или Python не найден" }
Write-Output ("git-хуки: " + (git config core.hooksPath))
