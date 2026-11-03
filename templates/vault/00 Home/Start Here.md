---
type: home
status: active
tags: [home]
---

# Start here

This folder is your **notes vault**. Write and edit notes here with Obsidian or any text editor.
The Second Brain reads this folder (it never writes to it) and uses your notes as knowledge when it answers.

## Folders

| Folder | What goes in it | Template |
|---|---|---|
| 00 Home | This page, dashboards, maps | — |
| 01 Inbox | Quick captures, not filed yet | Inbox Item |
| 02 Daily | One note per day (YYYY-MM-DD) | Daily Note |
| 03 Company | Company profile, strategy, operations | Company Note |
| 04 Services | What you offer | Service |
| 05 Clients | One subfolder per client | Client, Contact |
| 06 Projects | One subfolder per project | Project |
| 07 Sales | Leads, opportunities, proposals | Opportunity |
| 08 Knowledge | Learnings, references, how-tos | Knowledge Note |
| 10 Meetings | Meeting notes | Meeting Note |
| 11 Decisions | Decision records | Decision Record |
| 12 Assets | Attachments (not indexed) | — |
| 13 Archive | Finished or inactive notes | — |
| 14 Systems | Architectures, automations, runbooks | System |
| 15 Personal | Personal notes (indexed only if you opted in) | Personal Note |
| 90 Templates | Note templates (not indexed) | — |

## Conventions that help the Second Brain

- Start every note from a template, so it has frontmatter: `type`, `date`, `status`, `tags`.
  The Second Brain reads these fields: "which decisions are still proposed?" works because of `status`.
- Keep the folder category meaningful: a decision goes in `11 Decisions`, a meeting in `10 Meetings`.
  Questions that name a category ("what did we decide…", "last meeting with…") favour notes from that folder.
- Link notes with `[[Note name]]`. Use one subfolder per client or project, with an anchor note of the same name.
- Daily notes are named `YYYY-MM-DD.md`.
- Never put passwords, API keys or tokens in notes: files that contain them are quarantined and not indexed.
- Notes whose file name starts with `_` (like `_About this folder.md`) are guides and are not indexed.

## How notes reach the Second Brain

1. Save a note here.
2. Run `sb ingest` (or the scheduled update, if you set one up): new and changed notes are indexed, deleted notes are removed.
3. Ask: `sb ask "..."` or the local web UI. Answers cite the note and line numbers.

In Obsidian, *Templates* (core plugin) is set to `90 Templates` and *Daily notes* to `02 Daily`.
In other editors, copy a template and replace `{{date}}` and `{{title}}` by hand.
