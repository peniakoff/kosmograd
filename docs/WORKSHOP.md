# Workshop publish

## Current status

`workshop/` is a non-installable prototype catalog. Do not deploy the whole directory while `workshop/NOT_INSTALLABLE_YET.md` exists. P0 experiments should copy only the minimal disposable objects required for the current spike.

## Create the private WIP item (once)

1. Game → Workshop → Your items (WIP) → plus.
2. Name: `Kosmograd: Sputnik`.
3. Preview: `previewimage.png`, ≤ 1 MB (500×500 or 512×512 is the usual ask).
4. Description: paste `workshop/description.txt`.
5. Accept Steam workshop agreement in a browser if this is the first item (silent fail otherwise).
6. Close game. Open `SovietRepublic/media_soviet/workshop_wip/<ITEM_ID>/`.
7. During P0, copy only the minimal tested object definitions. After the release validator passes, copy the candidate `workshop/` contents and merge `workshopconfig.ini` without overwriting Steam identifiers.
8. Keep `$ITEM_ID` and `$OWNER_ID` in the live WIP folder, not in git.

## Preview image

Not generated in this repo yet. Required before public visibility. Soviet-concrete pad silhouette, no copyrighted spacecraft photos.

## Description rules

- Feature list for **what actually loads**.
- Grey-box limitations stated plainly in private and closed-test instructions.
- Tested game version pinned at the top.
- Load order: no vanilla edits; should not care. If it does, that is a bug.
- FAQ: gentle rail curves; professors required; not a real space sim.
- EN first. RU strings should ship only after review by a speaker; otherwise state that the first release is EN-only.

## Visibility

`$VISIBILITY 0` = private. Keep P0/P1 private and P2 in a closed beta. Public visibility starts only after representative art, three external test completions and an honest feature description.

## Release checklist (P6)

- [ ] Five screenshots: district, pad close-up, VAB, the exact verified endpoint, and logistics overview
- [ ] Short trailer if you have the footage; skip rather than fake
- [ ] Changelog
- [ ] Name search (NAMING.md banned list + "Kosmograd" clash)
- [ ] Semver: breaking saves only on major, bold in changelog
- [ ] Matrix in TESTING.md green
- [ ] `python tools/validate_workshop.py` passes
- [ ] `NOT_INSTALLABLE_YET.md` removed in the same release commit

## Updating

After release validation: change files in git `workshop/` → copy to `workshop_wip/<id>/` while preserving Steam metadata → in-game green check → run the gameplay test → upload. Do not edit only in the numbered folder.
