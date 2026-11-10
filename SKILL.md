---
name: image-material-library
description: Search, browse, inspect, maintain, and reuse the local 银行螺丝钉 PPT historical image library and its SQLite catalog. Use when the PPT team needs to find reusable images from public livestream, private livestream, or external-speech decks by keyword, title, episode, source, or image text; return usable local paths; maintain versions; operate the local Flask gallery; or continue building the PPT历史配图库.
---

# PPT历史配图库

Use the existing library at `/Users/fanlili/Desktop/范丽丽./图片素材库`. Treat this as the canonical working copy. Do not duplicate its multi-gigabyte image data inside the skill.

The library is a retrieval and reuse system for the PPT team. Its primary job is to find a useful historical slide image quickly by fuzzy keyword. Keep all pages except covers and final summary pages from public livestream PPT, private/high-net-worth PPT, and external-speech PPT. 螺丝钉学院 is retired from this library and must not be scanned, synchronized, imported, or re-added.

## Search and reuse

1. Run `python3 scripts/library_cli.py info` to verify the library.
2. For a normal keyword request, search the complete retained historical PPT corpus, not only the manually catalogued assets. Use the main gallery search or `/api/ppt-search?q=关键词`; fuzzy terms, aliases, and common misspellings are supported. Multiple terms use AND matching.
3. Search and rank page OCR text, deck titles, episode/date information, and paths. Results show where a page occurrence was found: public/private episode or unnumbered public专题 folder, external-speech date, and exported page number. Say “出现于”, not “唯一来源”, because a reusable slide may occur in multiple decks. Inspect promising images visually before selecting them.
4. Use the homepage “历史PPT分类” tree to browse the complete corpus by `内容主题`. A page may have multiple tags. A parent-node filter includes all descendants, and a taxonomy filter can be combined with a keyword.
5. Return absolute paths. Preserve source files; copy them into a project only when the user requests an editable deliverable.
6. Prefer a current catalogued version when the same image is maintained there. The searchable historical corpus is `ppt_jpegs` (公募直播), `private_jpegs` (私募/高净值直播), and `speech_jpegs` (对外演讲). `version_sheet_jpegs` stores current chart versions from 投顾&私募常用图表更新记录. Do not use `academy_jpegs`.

## Maintain the catalog

- Back up `library.db` before schema changes or bulk mutations.
- `page_taxonomy.py` applies the auditable tree taxonomy to all retained PPT pages using titles and OCR. Low-confidence unmatched pages go to `待细分`; never force a narrow classification without evidence. `inventory.py` refreshes the taxonomy after scanning.
- Open `/workbench` (“异常待确认”) only for evidence-backed exceptions such as missing/invalid page number, missing source, or explicit OCR failure. Normal historical PPT pages are searchable automatically and must not be sent through a manual import queue. The legacy `pending` count is not a workload metric. Resolve exceptions by correcting metadata, confirming the page should remain searchable, or explicitly excluding a confirmed non-PPT/cover/summary page; each resolution is audited.
- The main gallery “检测更新” button is the unified entry point: it recursively scans all files beneath the public-live, private-live, and external-speech Feishu shared folders, synchronizes embedded latest images from the “投顾&私募常用图表更新记录” spreadsheet, then scans those raw sources into the candidate inbox. Modified remote files are stored as update candidates and never overwrite older source images.
- Never run `sync_zsxq_academy.py` as part of library maintenance. Academy content is intentionally retired.
- Treat inbox states as a pipeline: `pending` → `imported` or `skipped`; exact matches become `duplicate_indexed` or `duplicate_raw`.
- Use the workbench visual-similarity filter to review perceptual-hash groups. The processor uses 64-bit pHash with a conservative Hamming threshold of 4 and representative-based grouping.
- Similarity groups are review candidates, not duplicate decisions. Review them by confidence: `high` means highly similar recurring speech-slide imagery; `medium` means likely recurring/template-related; `low` includes weak matches, shared cover templates, and different pages from the same PPT.
- Use the “高度相似 / 可能同模板 / 弱相似” filters to process the strongest candidates first. Confidence never changes inbox status automatically.
- Record a reviewed group as `versions`, `template`, `false_match`, or `uncertain`. Group review decisions persist across unchanged reclustering and are written to `audit_log`.
- The “作为版本” dialog recommends existing target assets from name, tag, source, and description overlap. Treat the ranking as a suggestion and verify the target before importing.
- Batch skip/restore applies only to explicitly checked members of the current group and requires a browser confirmation. Do not infer permission to process an unchecked member.
- Click a similarity-group thumbnail to open the large comparison viewer. Use side-by-side mode for content review, difference-overlay mode to locate changed regions, and arrow keys to rotate the right-hand image.
- In similarity-group review, compare members side by side and handle each image explicitly. Do not bulk-skip a group merely because its layout is similar.
- For a revised image of an existing catalog item, choose “作为版本”, search for the target asset, add a version note, and decide whether it becomes current. Prefer this over creating a duplicate-name asset.
- Adding an inbox item as a version copies the source image, preserves older versions, updates the inbox state, and records an audit event.
- Use automatic inbox suggestions as editable starting points. PPT paths yield episode/page sources; speech paths yield date/page sources; filename and OCR keywords map to existing catalog tags.
- Always review suggested names, sources, and tags before committing; suggestions never write metadata by themselves.
- OCR fields and text search are present, but run OCR only when a local `tesseract` executable is available; prefer `chi_sim+eng`.
- Use the existing import and patch scripts in the canonical directory. Read a script before running it and use its narrowest applicable mode.
- Keep tags hierarchical and concise. Preserve source links, modification times, and version history.
- Move catalog assets to `/recycle` instead of deleting files. Restore from the recycle bin when needed; tags and all versions remain intact.
- Record recycle and restore actions in `audit_log`.
- Use `/quality` to review missing source, link, description, duplicate names, and genuinely unused tags. Parent tags with active child tags are not considered unused.
- Save metadata corrections through the quality center; it supports editing the Feishu link in addition to name, source, and description.
- Never permanently delete or overwrite source images without explicit user authorization.

## Run the gallery

Run `python3 scripts/library_cli.py serve`. The gallery listens on the address printed by the command. Verify `/api/assets` before reporting it ready.
The main gallery is `/`; the pending-material workbench is `/workbench`; the metadata quality center is `/quality`; the progress dashboard is `/dashboard`.
Use `/health` for a lightweight service check. The Finder launcher starts the server with `nohup`, records a PID under `logs/`, and reuses an already-running service.
The first launch of each day creates an online SQLite backup under `backups/auto/`.

## Diagnose

- Read [references/layout.md](references/layout.md) for directory and database layout.
- If Flask is missing, install the requirement only after obtaining any required approval.
- Distinguish the indexed catalog from the raw corpus: the raw image count is expected to be much larger than the asset-table count.
