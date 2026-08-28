# Not installable yet

This directory is a prototype catalog, not a working Workshop item.

It currently contains annotated ini drafts and references files that do not exist yet, including meshes, materials, textures, icons and preview art. Several engine interactions are still awaiting the P0B spikes in `ROADMAP.md`.

Do not copy this directory into `media_soviet/workshop_wip/` expecting the game to load it.

Remove this file only when all of the following are true:

1. P0 records a `GO` decision in `docs/DECISIONS.md`.
2. Every object listed in `workshopconfig.ini` is intended for the candidate build.
3. Release validation reports no error other than the presence of this blocker file.
4. The candidate completes the relevant test script in `docs/TESTING.md`.

Remove this file in the release-candidate commit, then rerun `python tools/validate_workshop.py`; that run must pass.
