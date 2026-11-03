# Health & security checks (`sb doctor`)

[← Wiki home](../README.md) · Code: `doctor()` in `src/sb.py` · Threat model: [SECURITY.md](../SECURITY.md)

Run it under the sandbox so the boundary itself is tested: `<instance>/bin/sb-sandboxed doctor`. The first time, add `--record` to store model checksums. Exit code 0 = all PASS.

| Check | PASS means |
|---|---|
| permissions | Nothing in the instance folder is group/world accessible |
| sandbox: write to source root denied | Sources are read-only at the OS level |
| sandbox: read of out-of-scope fixture denied | A deliberately denied test folder cannot be read |
| sandbox: home listing denied | Nothing outside the allowed folders is readable |
| sandbox: outbound network denied | In local mode, a connection to 1.1.1.1:443 fails (hosted mode reports that egress is allowed by your choice) |
| sandbox: launching other programs denied | Inside the sandbox, `/usr/bin/true` and `/usr/bin/open` cannot be started: only the launchers and the instance Python may run. A FAIL that says the profile has no process-exec rules means the instance predates this check; re-run the setup wizard to regenerate the profile |
| sandbox: reads allowed / writes allowed | Your folders are readable; the instance is writable |
| ollama reachable · models installed | Ollama on 127.0.0.1:11434; required models present |
| checksum: digest unchanged | Model digests match those recorded by `--record` (tamper/upgrade detection) |
| sockets: loopback only | Ollama and the UI listen on 127.0.0.1 only |
| disk ≥ 50 GB free | Room for indexes, backups and models |
| index: no .env/.npmrc content · no paths outside roots | Exclusions held |
| system card refreshed | [System card](08-knowledge.md#system-card) updated |

Results are also written to `logs/doctor.jsonl`.

**A lesson built in:** a Seatbelt rule like `(allow network* (local ip "localhost:*"))` matches *every* outbound socket (its local side is always this machine). The templates allow only `network-outbound` to a loopback **remote** address, and doctor's 1.1.1.1 test catches regressions.
