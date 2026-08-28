# Sync git `workshop/` → Steam WIP

Steam path (Windows typical):

```text
<steam>/steamapps/common/SovietRepublic/media_soviet/workshop_wip/<ITEM_ID>/
```

## Steps

1. Create the WIP item in-game once. Note `<ITEM_ID>`.
2. Copy everything from `workshop/` into that folder **except** do not replace `$ITEM_ID` / `$OWNER_ID` / `$ITEM_TYPE` if Steam already wrote them. Merge `$OBJECT_*` lines from git.
3. Never copy `*.bbox`, `*.fire`, `bbox.bin`, `preview.dds` from git (they should not be in git).
4. Boot the game, open the WIP item, green check to save.
5. After ModelViewer writes `.nmf` / `.mtl` / `.dds` into the WIP folder, copy those binaries **back** into git `workshop/...` if you want them versioned — or leave them local. Meshes can wait until they are not cubes.

If `$OBJECT_BUILDING buildings/kosm_…` does not show in-game, flatten: move each asset folder to the WIP root and change tokens to `$OBJECT_BUILDING kosm_rocket_factory`. Record the working form in `docs/DECISIONS.md`.
