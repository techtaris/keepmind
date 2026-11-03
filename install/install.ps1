<#
.SYNOPSIS
  Installs Second Brain prerequisites on Windows (winget + npm + ollama).
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install.ps1 -Component check
  powershell -ExecutionPolicy Bypass -File install.ps1 -Component python
  powershell -ExecutionPolicy Bypass -File install.ps1 -Component models -ChatModel llama3.1:8b -EmbedModel nomic-embed-text
.NOTES
  Every action prints the exact command before running it. Nothing is installed with -Component check.
#>
param(
  [ValidateSet("check","python","ollama","models","git","node","claude","codex","pywebview","all")]
  [string]$Component = "check",
  [string]$ChatModel = "llama3.1:8b",
  [string]$EmbedModel = "nomic-embed-text"
)
$ErrorActionPreference = "Stop"

function Run([string]$exe, [string[]]$argv) {
  Write-Host ">> $exe $($argv -join ' ')"
  & $exe @argv
  if ($LASTEXITCODE -ne 0) { throw "command failed ($LASTEXITCODE): $exe" }
}
function Has([string]$name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }
function Winget([string]$id) {
  if (-not (Has "winget")) { throw "winget is not available. Install 'App Installer' from the Microsoft Store, then re-run." }
  Run "winget" @("install", "--exact", "--id", $id, "--accept-package-agreements", "--accept-source-agreements")
}
function FindPython {
  foreach ($c in @("py -3.12", "py -3", "python")) {
    $parts = $c.Split(" ")
    if (Has $parts[0]) {
      $v = & $parts[0] @($parts[1..9]) -c "import sys,sqlite3;sqlite3.connect(':memory:').execute('create virtual table t using fts5(x)');print(sys.version_info>=(3,10))" 2>$null
      if ($v -eq "True") { return $c }
    }
  }
  return $null
}
function Status {
  $py = FindPython
  $ollama = $null; try { $ollama = (Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/version" -TimeoutSec 3).version } catch {}
  [ordered]@{
    python  = if ($py) { "ok ($py)" } else { "missing" }
    ollama  = if ($ollama) { "ok ($ollama)" } elseif (Has "ollama") { "installed, not running" } else { "missing" }
    git     = if (Has "git") { "ok" } else { "missing (optional)" }
    node    = if (Has "npm") { "ok" } else { "missing (needed for claude/codex CLIs)" }
    claude  = if (Has "claude") { "ok" } else { "missing (optional)" }
    codex   = if (Has "codex") { "ok" } else { "missing (optional)" }
  } | ConvertTo-Json
}

switch ($Component) {
  "check"     { Status }
  "python"    { Winget "Python.Python.3.12" }
  "ollama"    { Winget "Ollama.Ollama"; Write-Host "Start Ollama from the Start menu (it listens on 127.0.0.1:11434)." }
  "git"       { Winget "Git.Git" }
  "node"      { Winget "OpenJS.NodeJS.LTS" }
  "models"    { if (-not (Has "ollama")) { throw "Install Ollama first." }
                Run "ollama" @("pull", $EmbedModel); if ($ChatModel) { Run "ollama" @("pull", $ChatModel) } }
  "claude"    { if (-not (Has "npm")) { throw "Install Node.js first (-Component node)." }; Run "npm" @("install", "-g", "@anthropic-ai/claude-code") }
  "codex"     { if (-not (Has "npm")) { throw "Install Node.js first (-Component node)." }; Run "npm" @("install", "-g", "@openai/codex") }
  "pywebview" { $py = FindPython; if (-not $py) { throw "Install Python first." }
                $p = $py.Split(" "); Run $p[0] (@($p[1..9]) + @("-m", "pip", "install", "--user", "pywebview")) }
  "all"       { Winget "Python.Python.3.12"; Winget "Ollama.Ollama"; Winget "Git.Git"
                Write-Host "Restart the terminal so PATH updates apply, start Ollama, then run: install.ps1 -Component models" }
}
