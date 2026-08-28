# References

## Game / modding

- Hooded Horse — General modding  
  https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding
- LovelyPL — Buildings `SCRIPT.INI` / `building.ini` tokens  
  https://steamcommunity.com/sharedfiles/filedetails/?id=1885817861
- LovelyPL — Vehicles `script.ini`  
  https://steamcommunity.com/sharedfiles/filedetails/?id=1861143159
- Steam — Beginner modders Q&A  
  https://steamcommunity.com/sharedfiles/filedetails/?id=2050253358
- Getting started with asset creation (files actually required)  
  https://steamcommunity.com/app/784150/discussions/0/2244426186191135241/

These guides are useful but not sufficient proof. The vehicle guide may also appear removed or incompatible in Steam while its text remains readable. For implementation, the precedence order is:

1. Observed behavior on the game build pinned in `TESTING.md`.
2. A vanilla object from that exact build using the same type and token context.
3. Current official wiki guidance.
4. Community/Steam token guides, with their revision date recorded.
5. This repository's hypotheses.

Every P0 spike records the relevant vanilla path and minimal diff so a future game update can be retested without relying on memory.

## Tools

- Blender manual — OBJ export, UV, applied transforms  
  https://docs.blender.org
- paint.net / GIMP — DDS plugins as required by your version

## Design sources for this merge

- Internal MD: *Kosmograd: Sputnik – WR:SR Mod Development Master Plan* (MVP loop, airplane/cargo/rail tricks)
- Internal PDF: *Kosmograd Mod Design & Development Plan v1.0, August 2026* (pillars, naming, grey-box, full district, Glory-as-design-target)

The merge itself is [DECISIONS.md](DECISIONS.md). Do not treat the PDF JSON snippets or the MD's invented tokens as loadable files.
