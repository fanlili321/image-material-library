---
name: image-material-library
description: Search and maintain a user-authorized local image-material library for PPT production. Use when the user asks to find reusable images or inspect a local PPT visual corpus; do not use it to source unlicensed web images.
---

# Image Material Library

Search a user-authorized local image library and return reusable candidates with enough context for the user to verify them.

## Before searching

- Ask for or confirm the library root, unless it is already provided in the task.
- Treat the library as user-owned material. Do not copy its contents into the Skill package or publish it.
- Inspect available filenames, metadata, manifests, or a local index first. Do not assume a particular database schema or folder layout.

## Search workflow

1. Translate the requested concept into a small set of precise keywords and visual criteria.
2. Search the authorized library using its local index when available; otherwise search filenames and folders conservatively.
3. Return candidate paths, previews when appropriate, and a brief reason each candidate fits.
4. Preserve originals. For renames, reorganization, or deletion, show the exact target and obtain confirmation before changing files.

## Boundaries

- This public Skill contains no image corpus, user paths, private indexes, or prior-project materials.
- Do not use results beyond the user-authorized library or imply that their license transfers to other uses.
- If no authorized library is available, ask the user to provide a folder or source rather than fabricating an asset inventory.

