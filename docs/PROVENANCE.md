# Asset and source provenance

The repository license applies to original Kosmograd material contributed under that license. It does not relicense third-party game files, tools, fonts, textures, reference images or other external material.

## Vanilla definitions

- Vanilla WR:SR files are local technical references.
- Do not commit an unchanged vanilla file merely to use it as a template.
- For every implemented asset, record the pinned game build, vanilla relative path and a minimal diff or list of changed fields in the P0 evidence note.
- If a functional definition must retain substantial vanilla content for compatibility, verify redistribution terms before public release and document the basis here.

## Models, textures and audio

Each final asset must record:

| Field | Required value |
|---|---|
| Author | Person or tool-assisted contributor |
| Source | Original work or exact external reference URL/path |
| License / permission | SPDX identifier, explicit permission, or `original` |
| AI assistance | Tool and role, if any |
| Derivatives | Source asset and material changes |

Historical photographs and spacecraft drawings may be references without becoming redistributed textures. Do not trace or package copyrighted art unless its license permits the intended use.

## Generated and local files

Generated game bounds and previews listed in `.gitignore` are not sources. Blender, ModelViewer and image-editor outputs intended for release may be committed only with the provenance of their inputs recorded.

## Legacy, unshipped source drafts

The three files under `blender/legacy/p1-concepts/` were recovered from commit
`a7c8cd5` authored by Tomasz Miller. They contain no linked bitmap textures and
are retained only for geometry salvage. Exact modelling-tool assistance was
not recorded on the historical branch, so these files are **not cleared for
release**. Before derived geometry becomes canonical, confirm its authorship,
record any AI or procedural assistance, and add the resulting asset-specific
entry here.

## Release gate

Before public Workshop visibility, every shipped binary and texture must have a provenance entry and no unresolved `unknown` license status.
