# Notes vault (Obsidian or any Markdown editor)

[← Wiki home](../README.md) · Code: `vault_init.py`, `templates/vault/`, `src/sb.py` (`vault_of`, `vault_category`, `vault_tier`, `frontmatter`, `knowledge_vault`), `setup_wizard.py` (notes vault step)

A **notes vault** is one folder of Markdown notes that *you* write and edit, with Obsidian or any text editor, on macOS, Windows or Linux.
The second brain **reads** it as knowledge and **never writes to it**: save a note, run `sb ingest`, and the note is part of the answers, with citations to the file and lines.

## Folder layout

| Folder | What goes in it | Template | Category | Indexed |
|---|---|---|---|---|
| 00 Home | Start page, dashboards, maps | — | `home` | yes |
| 01 Inbox | Quick captures, not filed yet | Inbox Item | `inbox` | yes |
| 02 Daily | One note per day, `YYYY-MM-DD.md` | Daily Note | `daily` | yes |
| 03 Company | Company profile, strategy, operations | Company Note | `company` | yes |
| 04 Services | What you offer | Service | `services` | yes |
| 05 Clients | One subfolder per client, with an anchor note | Client, Contact | `clients` | yes, unless you turn client notes off |
| 06 Projects | One subfolder per project, with an anchor note | Project | `projects` | yes |
| 07 Sales | Leads, opportunities, proposals | Opportunity | `sales` | like 05 Clients |
| 08 Knowledge | Learnings, references, how-tos | Knowledge Note | `knowledge` | yes |
| 10 Meetings | Meeting notes | Meeting Note | `meetings` | yes |
| 11 Decisions | Decision records | Decision Record | `decisions` | yes |
| 12 Assets | Attachments | — | `assets` | no |
| 13 Archive | Finished or inactive notes | — | `archive` | yes |
| 14 Systems | Architectures, automations, runbooks | System | `systems` | yes |
| 15 Personal | Health, travel, life | Personal Note | `personal` | **no**, unless you opt in |
| 90 Templates | Note templates (placeholders only) | — | `templates` | no |

Each folder has an `_About this folder.md` guide note; files whose name starts with `_` are never indexed. `00 Home/Start Here.md` explains the conventions.
The templates carry YAML frontmatter (`type`, `date`, `status`, `tags`) and use Obsidian's core *Templates* placeholders `{{date}}`, `{{time}}`, `{{title}}`.
The starter `.obsidian/` settings point *Templates* to `90 Templates`, *Daily notes* to `02 Daily`, attachments to `12 Assets` and new notes to `01 Inbox`. In another editor, copy a template and fill the placeholders by hand.

## Creating or completing a vault
- **Setup wizard / desktop installer:** choose *Create a new vault* (default `~/SecondBrain-Vault`, or `%USERPROFILE%\SecondBrain-Vault` on Windows), *Use an existing vault*, or *No vault*. The vault is added to the source folders automatically.
- **By hand:** `python3 vault_init.py <folder>` creates the vault, or adds only what is missing to an existing one. `--dry-run` lists what would be created. It never overwrites, renames or deletes anything, and it leaves an existing `.obsidian/` folder untouched.

The same folder rules as for source folders apply: credential, app-data and cloud-sync locations (iCloud Drive, OneDrive, Dropbox, Google Drive) are refused; Desktop/Documents need confirmation.

## How notes are read
1. **Category** = the first folder under the vault root, with the number prefix removed (`11 Decisions` → `decisions`). Unnumbered names are matched too (`Clients`, `Personal`, `Meetings`…); anything else is `notes`. Notes in the vault root are `home`.
   Map other folders in `config/secondbrain.json` → `vaults[].folder_map`, e.g. `{"AI": "knowledge", "copilot": "skip"}`.
2. **Tier:** vault notes are tier **V** (on whenever a vault is configured). `15 Personal` is tier P (off) unless `include_personal` is true; `05 Clients` and `07 Sales` become tier W (off) if `include_clients` is false. Templates, bases, canvas and assets are skipped (`vault-templates-assets` in the ingest log).
3. **Frontmatter** (`type`, `status`, `tags`, `date`, `client`, `project`, `owner`, `due`) is read and removed from the text (its lines are blanked, so line numbers in citations stay right). It is added to every chunk as one line, e.g.
   `[category: decisions | type: decision | status: proposed | tags: decision, database | date: 2026-10-01]`, so both search and the model see it.
4. **Wikilinks** `[[Note]]` / `[[Note|alias]]` / `![[image.png]]` become plain text, so quotes in answers match the note.
5. **Project** = `<vault>/<category folder>[/<subfolder>]`, e.g. `MyVault/05 Clients/Acme`, so every client or project subfolder gets its own project card.

Changing any vault setting re-reads the vault notes on the next ingest (only those; nothing else is re-embedded).

## Asking by category
- Questions that name a category (*decision*, *meeting*, *client*, *project*, *sales/lead*, *daily/today*, *inbox*, *system*, *service*, *company/strategy*; English and Spanish) give notes from that folder a ranking boost.
- Restrict to categories: `sb ask "what is still open?" --in decisions,meetings` (also `sb query … --in …`; the web UI API accepts `"in": [...]`).
- `knowledge/00 Home/vault-index.md` (rebuilt at the start of every ingest, straight from the files) lists every indexed note per category with type, status, date, tags and modified date, so questions like *"which decisions are still proposed?"* can be answered from it.

## Generated knowledge uses the same layout
`knowledge/` itself is laid out as a vault: `00 Home/` (system card, project map, inventory, vault index, `Home.md`), `06 Projects/` (project cards), `11 Decisions/`. It has its own `.obsidian/`, so you can open it as a separate, read-only vault in Obsidian. Older instances are moved to this layout automatically (`maps/` → `00 Home/`, `projects/` → `06 Projects/`, `decisions/` → `11 Decisions/`).

## Health checks
`sb doctor` checks that each vault is readable, and inside the sandbox that writing into the vault is denied.
