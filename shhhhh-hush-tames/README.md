# Shhhhh Hush Tames

![Shhhhh Hush Tames logo](./assets/logo.png)

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
