# Contributing

This is a small, opinionated catalog. New content follows existing docs; it does not reopen the merge.

## Add or change an asset

1. Edit `docs/ASSETS.md` first (footprint, tokens, sockets, tris). That commit can stand alone.
2. Grey-box in `blender/assets/...` per `docs/BLENDER.md`.
3. Fill `workshop/...` from vanilla ini + ModelViewer output.
4. Add or confirm the `$OBJECT_*` line in `workshop/workshopconfig.ini`.
5. Line in `CHANGELOG.md` under Unreleased.
6. Run the relevant rows of `docs/TESTING.md`.

Do not add P3 folders to `workshop/` until P3 is started. Sheets in ASSETS.md are enough.

## Ini edits

Copy vanilla. No REJECTED tokens. No spaces outside quotes. If a token is UNVERIFIED, comment it and list the spike.

## Art

Budgets in ASSETS.md are ceilings. Shared atlas. No interiors. No static rocket on the pad stand.

## Language

Docs are English. In-game `$NAME_STR` English until P5 RU pass.
