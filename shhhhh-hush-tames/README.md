# Shhhhh Hush Tames

**Shhhhh Hush Tames** is a lightweight quality-of-life mod that lets each player control supported tame sound muting through persistent global shoulder, riding, and mating preferences.

## Overview

This mod is intended for players who want quieter shoulder pets, ridden creatures, and mating pens without lowering all game sound or remapping creatures.

The current early test version is focused on the core player preference system:

- per-player persistent global mute preferences
- shoulder mute defaults
- ridden mute defaults
- `Enable Mating` mute defaults
- in-game radial menu configuration

At the moment, the first public build is primarily being used to validate the persistence flow, radial menu workflow, and audio replacement strategy before broader creature coverage is added.

The long-term goal is broader official creature coverage plus more granular control through per-class, per-creature, and area-based muting rules.

## Current Scope

- Preferences are player-specific, not server-wide.
- Settings are stored on the player and persist between sessions.
- Current first-version implementation is focused on the creatures currently listed in the public coverage tracker and only applies through the global shoulder, riding, and mating preferences.
- No creature class remaps or dino replacements are used.
- Wild and hostile creature audio is not the target of this mod.

## Configuration

This version does **not** use `GameUserSettings.ini`.

Settings are stored as persistent player data and configured in-game through the radial menu.

## Coverage Tracker

See [Tracker](./tracker.md).

## Tracker Sync

This repo includes a local sync script that rebuilds `tracker.md` directly from the Notion tracker without using ChatGPT.

Files:

- `sync_tracker_from_notion.py`
- `.env.example`

Setup:

1. Copy `.env.example` to `.env`
2. Set `NOTION_TOKEN`
3. Keep `NOTION_TRACKER_DATA_SOURCE_ID` as-is unless the Notion data source changes

Run:

```powershell
python .\sync_tracker_from_notion.py
```

Optional:

```powershell
python .\sync_tracker_from_notion.py --stdout
python .\sync_tracker_from_notion.py --output .\tracker.md
```

What it does:

- queries the Notion Tracker data source through the Notion REST API
- paginates through all rows
- sorts by group, creature name, and variant
- regenerates `tracker.md` with the repo’s current markdown structure

The tracker is intended both as a development checklist and as a public coverage reference so players can see:

- which creatures are still only planned
- which creatures are already in the internal data table
- which creatures are already included in the current CurseForge release
- which sound categories are already isolated for each creature
- which creatures still need coverage work

## Current Limitations

- Individual per-creature overrides are not implemented yet.
- Per-class overrides are not implemented yet.
- Area-based muting with a structure is not implemented yet.
- Players cannot yet choose sound categories manually per creature, per class, or per sound profile.
- Configuration is currently handled through the radial menu only.
- The current public test implementation is limited to early creature coverage.

## Known Notes

- This is an early public test build and behavior may change as the mod expands to more creatures.
- Some creatures may require extra work to isolate specific sound cues cleanly.
- More granular controls are planned for future versions, including per-sound-type behavior, class overrides, creature overrides, and area-based filtering.

## Planned Features

- Per-creature mute overrides
- Per-class mute overrides
- Area-based muting through a placed structure
- Per-sound-type behavior rules for shoulder, riding, and mating
- Expanded coverage for official tameable creatures
- Override lists for classes and individual creatures that have already been customized

## Changelog

Release changelogs are available on the mod's CurseForge page.

## Community

[![Join our Discord](https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/6hNubWkU)

Get updates, share suggestions, and report bugs.
