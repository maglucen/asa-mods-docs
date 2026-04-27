# Drakeling Tweaks Compatibility

## Creature replacement

Drakeling Tweaks does not replace or remap the Drakeling.

This means it should work with existing and future Drakelings, as long as the underlying Drakeling class and relevant ability behavior remain compatible.

## Scope

The mod affects:

- tamed and unclaimed creature kill XP behavior;
- selected Drakeling cooldowns;
- optional buff info display;
- optional Hoard Chest disabling when stored XP is awarded;
- carried shoulder vocal sound toggling.

The mod does not change wild creature kill XP.

## Known bugs

- When the Drakeling is on the shoulder and muted, there is still one idle sound out of five that triggers from time to time.
- Even when `DisableHoardChests` is set to `True`, the HUD may still indicate that XP and a Dragon Key will be awarded. This is only a visual message; no chest/key is actually granted. The message appears to be hardcoded and has not been removed without remapping the Drakeling.

## Load order

No special load order is currently required.

If another mod heavily modifies the same Drakeling ability behavior, test both mods together before using them on a live server.
