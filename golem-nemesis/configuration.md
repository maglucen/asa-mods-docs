# Golem Nemesis Configuration

Add the following section to `GameUserSettings.ini`.

```ini
[GolemNemesis]
DamagePercentage=100
```

## Settings

### `DamagePercentage`

Controls the damage percentage used for the boosted anti-golem interactions covered by the mod.

- `100` = normal damage against the affected golems.
- `10` = Wildcard's default behavior.
- `200` = double normal damage.
- Values below `10` are clamped to `10`.
- Values above `100` are allowed.

## Behavior notes

- The configurable percentage applies to Doedicurus, Ankylosaurus, and Dunkleosteus.
- The mod affects Rock Golems and child classes such as Chalk Golems and Ice Golems.
- Internally, the mod restores the selected creatures from Wildcard's reduced anti-golem damage to a normal-damage baseline, then applies the configured percentage on top of that baseline.

## Editing notes

- Stop the server before editing config values.
- Save the file and restart the server after making changes.
- Keep the config under the `[GolemNemesis]` section.
