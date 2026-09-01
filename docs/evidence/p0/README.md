# P0 evidence

These reports are the release record for P0A and S1–S7. `NOT RUN` is deliberate: a fixture is not evidence until it has passed ModelViewer conversion, `verify --no-dlc`, and the observable in-game procedure.

Pinned automated environment: Steam build `23935965`, Fedora Linux 44 (`7.1.10-200.fc44.x86_64`), Blender `5.2.0 LTS`, ModelViewer through Proton 11. World Maps is installed only as a syntax reference; the final run must have it disabled.

Generate a report with the hashes of the exact staged item:

```bash
python tools/p0_harness.py snapshot --spike S1 --wip /path/to/workshop_wip/ITEM --out docs/evidence/p0/S1.md
```

Before recording an observation:

```bash
python tools/p0_harness.py verify --spike S1 --wip /path/to/workshop_wip/ITEM --no-dlc
```

Record private save and recording paths locally. Commit only their SHA-256 checksums and compressed screenshots.

| Report | State | Gate |
|---|---|---|
| [P0A](P0A.md) | `NOT RUN` | Pipeline prerequisite |
| [S1](S1.md) | `NOT RUN` | STOP on failure |
| [S2](S2.md) | `NOT RUN` | Primary or fallback required |
| [S3](S3.md) | `NOT RUN` | Primary or fallback required |
| [S4](S4.md) | `NOT RUN` | PIVOT on failure after working transport |
| [S5](S5.md) | `NOT RUN` | Non-blocking scope gate |
| [S6](S6.md) | `NOT RUN` | Non-blocking scope gate |
| [S7](S7.md) | `NOT RUN` | One-item or split packaging required |
| [Decision](DECISION.md) | `NOT MADE` | GO / PIVOT / STOP |
