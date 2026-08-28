# Workshop publish

## Create the WIP item (once)

1. Game → Workshop → Your items (WIP) → plus.
2. Name: `Kosmograd: Sputnik`.
3. Preview: `previewimage.png`, ≤ 1 MB (500×500 or 512×512 is the usual ask).
4. Description: paste `workshop/description.txt`.
5. Accept Steam workshop agreement in a browser if this is the first item (silent fail otherwise).
6. Close game. Open `SovietRepublic/media_soviet/workshop_wip/<ITEM_ID>/`.
7. Copy contents of this repo's `workshop/` **into** that folder (merge `workshopconfig.ini`: keep Steam's IDs, keep our `$OBJECT_*` lines).
8. Put `<ITEM_ID>` into the comment at the top of `workshop/workshopconfig.ini` in git so nobody guesses.

## Preview image

Not generated in this repo yet. Required before a public WIP. Soviet-concrete pad silhouette, no copyrighted spacecraft photos.

## Description rules

- Feature list for **what actually loads**.
- "Grey-box" said out loud until P2 is done.
- Tested game version pinned at the top.
- Load order: no vanilla edits; should not care. If it does, that is a bug.
- FAQ: gentle rail curves; professors required; not a real space sim.
- EN first. RU strings for `$NAME_STR` can wait until P5 but should be in the same commit as 1.0.

## Visibility

`$VISIBILITY 0` = private. Public WIP from P1 exit. Full release at P5.

## Release checklist (P5)

- [ ] Five screenshots: district, pad close-up, VAB, a launch (or honest consume), grey-box comparison if art shipped late
- [ ] Short trailer if you have the footage; skip rather than fake
- [ ] Changelog
- [ ] Name search (NAMING.md banned list + "Kosmograd" clash)
- [ ] Semver: breaking saves only on major, bold in changelog
- [ ] Matrix in TESTING.md green

## Updating

Change files in git `workshop/` → copy to `workshop_wip/<id>/` → in-game green check to save the item → Steam upload. Do not edit only in the numbered folder.
