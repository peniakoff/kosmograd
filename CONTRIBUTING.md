# Contributing

This is a small, opinionated catalog. New content follows the P0 decision gate and current roadmap; it does not turn unverified behavior into a feature by repetition.

## Add or change an asset

1. Edit `docs/ASSETS.md` first (footprint, tokens, sockets, tris). That commit can stand alone.
2. Grey-box in `blender/assets/...` per `docs/BLENDER.md`.
3. Fill `workshop/...` from vanilla ini + ModelViewer output.
4. Add the `$OBJECT_*` line only when the asset is part of the next candidate build.
5. Line in `CHANGELOG.md` under Unreleased.
6. Run `python tools/validate_workshop.py --prototype` and the relevant rows of `docs/TESTING.md`.
7. Update `docs/PROVENANCE.md` for any non-trivial external or AI-assisted source material.

Legacy P3 prototype folders already in `workshop/` are a design catalog, not shipped scope. Do not add new P3/P4 objects to `workshopconfig.ini` until the relevant phase starts.

## Ini edits

Copy from the named vanilla object in the pinned game build. Record the source path. No REJECTED tokens. No spaces outside quotes. Track separately whether a token is documented, valid in this context and verified in game.

## Art

Budgets in ASSETS.md are ceilings. Shared atlas. No interiors. No static rocket on the pad stand.

## Language

Docs are English. In-game `$NAME_STR` English until the public-release localization pass.

## Release readiness

Do not remove `workshop/NOT_INSTALLABLE_YET.md` until the P0 decision is `GO`, release validation passes and the core test loop is green. Prototype ini files may contain explanatory comments; a release candidate may not contain placeholder instructions.
