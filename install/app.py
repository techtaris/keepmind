#!/usr/bin/env python3
"""Second Brain — desktop installer.

A small Tauri-style desktop app: a Python backend (standard library) serving an HTML UI on 127.0.0.1,
shown in a native window when `pywebview` is installed, otherwise in your default browser.

It lets you:
  1. check and install prerequisites (install.ps1 / install.bat on Windows, install.sh on macOS/Linux);
  2. pick the isolated source folders ("vaults") and the instance folder with a native folder dialog;
  3. choose the LLMs: local Ollama models, Claude or OpenAI APIs, and an optional Claude Code / Codex operator;
  4. review the permissions and run the setup wizard (setup_wizard.py) non-interactively;
  5. run doctor / ingest / eval / the full pipeline on the new instance.

Security: binds to 127.0.0.1 only, per-launch token, Host-header check, and only allow-listed commands
(no free-form shell). Nothing is installed or created without a click.

Usage:  python3 install/app.py [--no-window] [--port N]
"""
import argparse, http.server, json, os, platform, re, secrets, shutil, socket, sqlite3, subprocess, sys, threading, time, urllib.request, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)
import setup_wizard as wiz  # noqa: E402  (reuses folder rules; its main() is not run)

OS = platform.system()
IS_WIN, IS_MAC = OS == "Windows", OS == "Darwin"
HOME = os.path.expanduser("~")
MODEL_RX = re.compile(r"^[A-Za-z0-9._:/@+-]{1,120}$")
ENV_RX = re.compile(r"^[A-Z_][A-Z0-9_]{0,63}$")
COMPONENTS = ["python", "ollama", "models", "git", "node", "claude", "codex", "pywebview"]
JOBS, WINDOW = {}, {"w": None}
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# ----------------------------------------------------------------------------- environment checks
def wizard_python():
    """A Python >= 3.10 with SQLite FTS5 for the wizard and sb (this one if it qualifies)."""
    cands = [[sys.executable]] + ([["py", "-3"], ["python"]] if IS_WIN else [["/opt/homebrew/bin/python3.12"], ["/opt/homebrew/bin/python3"], ["/usr/local/bin/python3"], ["python3"]])
    probe = 'import sys,sqlite3; assert sys.version_info>=(3,10); sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)"); print(sys.executable)'
    for c in cands:
        exe = shutil.which(c[0]) or (c[0] if os.path.isfile(c[0]) else None)
        if not exe: continue
        try:
            r = subprocess.run([exe] + c[1:] + ["-c", probe], capture_output=True, text=True, timeout=10)
            if r.returncode == 0 and r.stdout.strip(): return r.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None

def ollama_info():
    try:
        with _OPENER.open("http://127.0.0.1:11434/api/version", timeout=3) as r: ver = json.loads(r.read()).get("version")
        with _OPENER.open("http://127.0.0.1:11434/api/tags", timeout=5) as r: models = [m["name"] for m in json.loads(r.read()).get("models", [])]
        return ver, models
    except Exception:  # noqa: BLE001
        return None, []

def state():
    py = wizard_python(); ver, models = ollama_info()
    try:
        sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)"); fts = True
    except sqlite3.Error:
        fts = False
    has = lambda n: bool(shutil.which(n))  # noqa: E731
    prereqs = [
        {"id": "python", "label": "Python ≥ 3.10 + SQLite FTS5", "required": True, "ok": bool(py), "detail": py or "not found"},
        {"id": "ollama", "label": "Ollama (127.0.0.1:11434)", "required": True, "ok": bool(ver),
         "detail": f"running, v{ver}" if ver else ("installed, not running: start the Ollama app" if has("ollama") else "not installed")},
        {"id": "models", "label": "Ollama models", "required": True, "ok": bool(models), "detail": ", ".join(models) or "none pulled yet"},
        {"id": "sandbox", "label": "OS sandbox (macOS Seatbelt)", "required": IS_MAC, "ok": os.path.exists("/usr/bin/sandbox-exec"),
         "detail": "built into macOS" if IS_MAC else "not available on this OS: sb runs without an OS sandbox", "installable": False},
        {"id": "git", "label": "git", "required": False, "ok": has("git"), "detail": shutil.which("git") or "optional"},
        {"id": "node", "label": "Node.js / npm", "required": False, "ok": has("npm"), "detail": shutil.which("npm") or "needed only for Claude Code / Codex CLIs"},
        {"id": "claude", "label": "Claude Code CLI", "required": False, "ok": has("claude"), "detail": shutil.which("claude") or "optional: operator agent and sb validate"},
        {"id": "codex", "label": "Codex CLI", "required": False, "ok": has("codex"), "detail": shutil.which("codex") or "optional: operator agent"},
    ]
    try:
        import webview  # noqa: F401
        pv = True
    except ImportError:
        pv = False
    prereqs.append({"id": "pywebview", "label": "pywebview (native window)", "required": False, "ok": pv, "detail": "installed" if pv else "optional: without it this UI opens in your browser"})
    return {"os": OS, "home": HOME, "repo": REPO, "fts5_here": fts, "default_instance": os.path.join(HOME, "SecondBrain-Instance"),
            "default_vault": os.path.join(HOME, "SecondBrainVault"),
            "prereqs": prereqs, "ollama_models": models, "installer": "install.ps1" if IS_WIN else "install.sh"}

# ----------------------------------------------------------------------------- jobs (allow-listed commands, streamed output)
def start_job(title, argv, env=None, cwd=None):
    jid = secrets.token_hex(6); job = {"id": jid, "title": title, "cmd": " ".join(argv), "lines": [], "done": False, "rc": None, "started": time.time()}
    JOBS[jid] = job
    def run():
        try:
            p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, bufsize=1,
                                 env={**os.environ, **(env or {})}, cwd=cwd or REPO)
            for line in p.stdout: job["lines"].append(line.rstrip("\n"))
            job["rc"] = p.wait()
        except OSError as e:
            job["lines"].append(f"ERROR: {e}"); job["rc"] = 127
        job["done"] = True
    threading.Thread(target=run, daemon=True).start()
    return jid

def installer_argv(component, chat, embed):
    if IS_WIN:
        ps = shutil.which("powershell") or shutil.which("pwsh") or "powershell"
        return [ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HERE, "install.ps1"),
                "-Component", component, "-ChatModel", chat, "-EmbedModel", embed]
    return ["bash", os.path.join(HERE, "install.sh"), component, "--chat-model", chat, "--embed-model", embed]

def instance_cmd(inst, args):
    """Returns (argv, env). F5: on Windows, never go through a .cmd file: cmd.exe re-parses arguments ("BatBadBut"),
    so text from the Ask box could run commands. Call the interpreter and sb.py directly instead."""
    if IS_WIN:
        py = wizard_python()
        if not py: raise ValueError("No suitable Python found.")
        env = {"SB_ROOT": inst, "TMPDIR": os.path.join(inst, "tmp"), "TEMP": os.path.join(inst, "tmp"), "DO_NOT_TRACK": "1", "NO_PROXY": "127.0.0.1,localhost"}
        return [py, "-I", "-B", os.path.join(REPO, "src", "sb.py")] + args, env
    return ["bash", os.path.join(inst, "bin", "sb-sandboxed")] + args, None

# ----------------------------------------------------------------------------- native folder picker
PICKER_TITLES = {"source": "Choose a source folder for the Second Brain", "instance": "Choose (or create) the instance folder",
                 "vault": "Choose the notes vault folder (Obsidian or any Markdown editor)"}

def pick_folder(kind):
    """F2: the dialog title is chosen server-side from a fixed list and handed to the OS as data, never as code."""
    title = PICKER_TITLES.get(kind, PICKER_TITLES["source"])
    w = WINDOW["w"]
    if w is not None:
        import webview
        r = w.create_file_dialog(webview.FOLDER_DIALOG)
        return r[0] if r else None
    try:
        if IS_MAC:
            r = subprocess.run(["osascript", "-e", "on run argv", "-e", "POSIX path of (choose folder with prompt (item 1 of argv))",
                                "-e", "end run", title], capture_output=True, text=True, timeout=600)
        elif IS_WIN:
            ps = ("Add-Type -AssemblyName System.Windows.Forms; $d=New-Object System.Windows.Forms.FolderBrowserDialog; "
                  "$d.Description=$env:SB_PICKER_TITLE; if($d.ShowDialog() -eq 'OK'){$d.SelectedPath}")
            r = subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps], capture_output=True, text=True, timeout=600,
                               env={**os.environ, "SB_PICKER_TITLE": title})
        else:
            r = subprocess.run(["zenity", "--file-selection", "--directory", f"--title={title}"], capture_output=True, text=True, timeout=600)
        p = r.stdout.strip().rstrip("/\\") if r.returncode == 0 else ""
        return p or None
    except (OSError, subprocess.TimeoutExpired):
        return None

def open_folder(p):
    if not os.path.isdir(p): return False
    subprocess.Popen(["open", p] if IS_MAC else (["explorer", p] if IS_WIN else ["xdg-open", p]))
    return True

# ----------------------------------------------------------------------------- create instance
def create(body):
    inst = os.path.abspath(os.path.expanduser(str(body.get("instance", "")).strip()))
    if not inst or inst == REPO or inst.startswith(REPO + os.sep):
        raise ValueError("The instance folder must be outside the Second Brain repository.")
    roots, allow_sensitive = [], False
    for r in body.get("roots", []):
        p, status, msg = wiz.classify_root(str(r.get("path", "")))
        if status == "refused": raise ValueError(f"{p}: {msg}")
        if status == "sensitive":
            if not r.get("confirmed"): raise ValueError(f"{p}: {msg}; tick its confirmation box to include it")
            allow_sensitive = True
        roots.append(p)
    vmode = body.get("vault_mode", "none")
    if vmode not in ("new", "existing", "none"): raise ValueError("unknown vault mode")
    vpath = str(body.get("vault_path", "")).strip()
    if vmode != "none":
        vp, status, msg = wiz.classify_root(vpath, must_exist=(vmode == "existing"))
        if status == "refused": raise ValueError(f"Vault {vp}: {msg}")
        if status == "sensitive":
            if not body.get("vault_confirmed"): raise ValueError(f"Vault {vp}: {msg}; tick its confirmation box")
            allow_sensitive = True
        vpath = vp
    if not roots and vmode == "none": raise ValueError("Add at least one source folder or a notes vault.")
    provider = body.get("provider", "ollama"); operator = body.get("operator", "none")
    if provider not in ("ollama", "anthropic", "openai"): raise ValueError("unknown backend")
    if operator not in ("none", "claude-code", "codex"): raise ValueError("unknown operator")
    chat, embed = str(body.get("chat_model", "")).strip(), str(body.get("embed_model", "nomic-embed-text")).strip()
    for m in [embed] + ([chat] if chat else []):
        if not MODEL_RX.match(m): raise ValueError(f"invalid model name: {m!r}")
    env = {"SB_NONINTERACTIVE": "1", "SB_INSTANCE": inst, "SB_ROOTS": os.pathsep.join(roots), "SB_PROVIDER": provider,
           "SB_OPERATOR": operator, "SB_CHAT_MODEL": chat or "llama3.1:8b", "SB_EMBED_MODEL": embed,
           "SB_ACCEPT": "yes" if body.get("granted") else "no", "SB_CONTINUE_MISSING": "yes" if body.get("continue_missing") else "no",
           "SB_ALLOW_SENSITIVE": "yes" if allow_sensitive else "no", "SB_VAULT_MODE": vmode, "SB_VAULT_PATH": vpath,
           "SB_VAULT_COMPLETE": "yes" if body.get("vault_complete", True) else "no",
           "SB_VAULT_PERSONAL": "yes" if body.get("vault_personal") else "no", "SB_VAULT_CLIENTS": "yes" if body.get("vault_clients", True) else "no"}
    if not body.get("granted"): raise ValueError("Confirm the permission summary first.")
    if provider != "ollama":
        hm, ke = str(body.get("hosted_model", "")).strip(), str(body.get("api_key_env", "")).strip()
        if not MODEL_RX.match(hm or "-"): raise ValueError("enter the hosted model id")
        if not ENV_RX.match(ke): raise ValueError("enter the NAME of the environment variable that holds the API key (not the key)")
        env.update(SB_HOSTED_MODEL=hm, SB_API_KEY_ENV=ke)
    py = wizard_python()
    if not py: raise ValueError("No suitable Python found: install Python first (step 1).")
    return start_job("Create instance", [py, "-I", "-B", os.path.join(REPO, "setup_wizard.py")], env=env), inst

# ----------------------------------------------------------------------------- HTTP server
class Handler(http.server.BaseHTTPRequestHandler):
    token = ""; allowed_hosts = set()
    def _send(self, code, obj=None, ctype="application/json", body=None):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Cache-Control", "no-store")
        if ctype.startswith("text/html"):
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
        self.end_headers(); self.wfile.write(body if body is not None else json.dumps(obj, ensure_ascii=False).encode())
    def _ok_host(self):
        return self.headers.get("Host", "") in self.allowed_hosts
    def log_message(self, *a): pass
    def do_GET(self):
        if not self._ok_host(): return self._send(403, {"error": "bad host"})
        if self.path.split("?")[0] == "/":
            if f"t={self.token}" not in self.path: return self._send(401, {"error": "missing token"})
            with open(os.path.join(HERE, "ui", "index.html"), "rb") as f: return self._send(200, ctype="text/html; charset=utf-8", body=f.read())
        if self.headers.get("X-SB-Token") != self.token: return self._send(401, {"error": "missing token"})
        if self.path == "/api/state": return self._send(200, state())
        m = re.match(r"^/api/job/([0-9a-f]{12})\?since=(\d+)$", self.path)
        if m and m.group(1) in JOBS:
            j = JOBS[m.group(1)]; s = int(m.group(2))
            return self._send(200, {"lines": j["lines"][s:], "next": len(j["lines"]), "done": j["done"], "rc": j["rc"], "title": j["title"], "cmd": j["cmd"]})
        return self._send(404, {"error": "not found"})
    def do_POST(self):
        if not self._ok_host(): return self._send(403, {"error": "bad host"})
        if self.headers.get("X-SB-Token") != self.token: return self._send(401, {"error": "missing token"})
        n = min(int(self.headers.get("Content-Length", 0) or 0), 100_000)
        try: body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError: return self._send(400, {"error": "bad json"})
        try:
            if self.path == "/api/pick-folder":
                p = pick_folder(str(body.get("kind", "source")))
                if p and body.get("check"):
                    ap, status, msg = wiz.classify_root(p); return self._send(200, {"path": ap, "status": status, "message": msg})
                return self._send(200, {"path": p})
            if self.path == "/api/check-folder":
                ap, status, msg = wiz.classify_root(str(body.get("path", ""))); return self._send(200, {"path": ap, "status": status, "message": msg})
            if self.path == "/api/vault-plan":
                mode = body.get("mode", "new")
                ap, status, msg = wiz.classify_root(str(body.get("path", "")), must_exist=(mode == "existing"))
                missing = len(wiz.vault_init.plan(ap)) if status != "refused" else 0
                return self._send(200, {"path": ap, "status": status, "message": msg, "missing": missing, "exists": os.path.isdir(ap)})
            if self.path == "/api/install":
                comp = body.get("component")
                if comp not in COMPONENTS: return self._send(400, {"error": "unknown component"})
                chat, embed = str(body.get("chat_model") or "llama3.1:8b"), str(body.get("embed_model") or "nomic-embed-text")
                if not (MODEL_RX.match(chat) and MODEL_RX.match(embed)): return self._send(400, {"error": "invalid model name"})
                return self._send(200, {"job": start_job(f"Install: {comp}", installer_argv(comp, chat, embed), cwd=HERE)})
            if self.path == "/api/create":
                jid, inst = create(body); return self._send(200, {"job": jid, "instance": inst})
            if self.path == "/api/run":
                inst = os.path.abspath(os.path.expanduser(str(body.get("instance", ""))))
                if not os.path.isfile(os.path.join(inst, "config", "secondbrain.json")): return self._send(400, {"error": "not a Second Brain instance folder"})
                action = body.get("action")
                acts = {"doctor": ["doctor", "--record"], "ingest": ["ingest"], "eval": ["eval", "--system"], "map": ["knowledge", "map"], "vault": ["knowledge", "vault"], "stats": ["stats"]}
                if action == "pipeline":
                    if IS_WIN: return self._send(400, {"error": "full pipeline script is bash-only; run ingest and eval on Windows"})
                    return self._send(200, {"job": start_job("Full pipeline", ["bash", os.path.join(inst, "bin", "run-all.sh")], cwd=inst)})
                if action == "ask":
                    q = str(body.get("question", "")).strip()[:500]
                    if not q: return self._send(400, {"error": "empty question"})
                    argv, env = instance_cmd(inst, ["ask", q])
                    return self._send(200, {"job": start_job("Ask", argv, env=env, cwd=inst)})
                if action not in acts: return self._send(400, {"error": "unknown action"})
                argv, env = instance_cmd(inst, acts[action])
                return self._send(200, {"job": start_job(action.capitalize(), argv, env=env, cwd=inst)})
            if self.path == "/api/open-folder":
                return self._send(200, {"ok": open_folder(os.path.abspath(os.path.expanduser(str(body.get("path", "")))))})
        except ValueError as e:
            return self._send(400, {"error": str(e)})
        return self._send(404, {"error": "not found"})

def main():
    ap = argparse.ArgumentParser(description="Second Brain desktop installer")
    ap.add_argument("--no-window", action="store_true", help="don't open a window or browser; just print the URL")
    ap.add_argument("--port", type=int, default=0)
    a = ap.parse_args()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    port = srv.server_address[1]
    Handler.token = secrets.token_hex(16); Handler.allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
    url = f"http://127.0.0.1:{port}/?t={Handler.token}"
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"Second Brain installer: {url}", flush=True)
    if a.no_window:
        try:
            while True: time.sleep(3600)
        except KeyboardInterrupt:
            return
    try:
        import webview
        WINDOW["w"] = webview.create_window("Second Brain — Setup", url, width=1120, height=880, min_size=(760, 600))
        webview.start()
    except ImportError:
        print("pywebview not installed: opening your browser instead (install it from step 1 for a native window).", flush=True)
        webbrowser.open(url)
        try:
            while True: time.sleep(3600)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
