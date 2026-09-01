# P0A — asset pipeline

| Field | Value |
|---|---|
| Steam build / DLC | `23935965` / final run with World Maps disabled |
| Vanilla source / SHA-256 | `buildings_types/gas_station.ini` / `700861707bf15546ce7fc64cb25cface3853afb3f229df3a0500a464279404b1` |
| INI diff | `experiments/p0/assets/p0_pipeline_shed/building.ini` |
| Source fixture / SHA-256 | `generated/p0_pipeline_shed/model.obj` / `931b251e680268b9edf553cb874820944d5aa2618432342df88fd6cec06b6e10` |
| Staged fixture hash | `UNSET — write with snapshot after ModelViewer conversion` |

Steps: convert `model.obj` to `model.nmf`/`material.mtl`, stage P0A, verify `--no-dlc`, launch twice, place twice, build once, and send a fuel truck to the single station. Check 4×6×3 m scale, +Z door, roof axis mark, generated bounds/fire, `Main` construction node and road access.

Observation: `NOT RUN`

Evidence screenshot / recording SHA-256: `UNSET`

Result: `NOT RUN`
