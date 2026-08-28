# Sync git `workshop/` → Steam WIP

Steam path (Windows typical):

```text
<steam>/steamapps/common/SovietRepublic/media_soviet/workshop_wip/<ITEM_ID>/
```

## Steps

1. Stop if `workshop/NOT_INSTALLABLE_YET.md` exists and you intend to copy the whole catalog. During P0, select only the disposable object under test.
2. Create the private WIP item in game once. Keep `<ITEM_ID>` in the Steam-owned folder.
3. Back up the live `workshopconfig.ini`.
4. Copy only the selected candidate files. Do not replace `$ITEM_ID`, `$OWNER_ID` or `$ITEM_TYPE`.
5. Merge only the selected `$OBJECT_*` lines into the Steam file.
6. Never copy `*.bbox`, `*.fire`, `bbox.bin`, `preview.dds` from git (they should not be in git).
7. Boot the game twice, inspect the object and record the result against the pinned game build.
8. After ModelViewer writes `.nmf` / `.mtl` / `.dds`, copy verified binaries back into the matching git asset folder only when they become part of a candidate build.

If `$OBJECT_BUILDING buildings/kosm_…` does not show in-game, flatten: move each asset folder to the WIP root and change tokens to `$OBJECT_BUILDING kosm_rocket_factory`. Record the working form in `docs/DECISIONS.md`.
