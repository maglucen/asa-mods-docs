# Grace Shield Configuration

Add the following section to `GameUserSettings.ini`.

```ini
[GraceShield]
TeleportProtectionSeconds=20.0
RespawnProtectionSeconds=20.0

bProtectTpedSurvivors=true
bProtectRespawnedSurvivors=true

bPreventIncomingDamage=true
bPreventOutgoingDamage=true
bPreventEnemyTargeting=true

bCancelProtectionOnAttack=false
bCancelProtectionOnMove=false
```

## Settings

### `TeleportProtectionSeconds`

Controls how long Grace Shield lasts after a detected survivor teleport.

- `20.0` = default teleport protection duration.
- `10.0` = 10 seconds of protection.
- `0.0` = no practical teleport protection window.

### `RespawnProtectionSeconds`

Controls how long Grace Shield lasts after a protected survivor respawns.

- `20.0` = default respawn protection duration.
- `10.0` = 10 seconds of protection.
- `0.0` = no practical respawn protection window.

### `bProtectTpedSurvivors`

When set to `true`, survivors can receive Grace Shield after a detected teleport.

When set to `false`, teleport protection for survivors is disabled.

### `bProtectRespawnedSurvivors`

When set to `true`, survivors can receive Grace Shield after respawning.

When set to `false`, respawn protection is disabled.

### `bPreventIncomingDamage`

When set to `true`, incoming damage is blocked while Grace Shield is active.

When set to `false`, protected survivors can still receive damage.

### `bPreventOutgoingDamage`

When set to `true`, protected survivors cannot deal damage while Grace Shield is active.

This prevents the grace window from being used offensively.

### `bPreventEnemyTargeting`

When set to `true`, wild creatures are prevented from targeting protected survivors during the grace window where supported by the game behavior.

### `bCancelProtectionOnAttack`

When set to `true`, Grace Shield is removed if the protected survivor attacks.

### `bCancelProtectionOnMove`

When set to `true`, Grace Shield is removed if the protected survivor moves.

## Editing Notes

- Stop the server before editing `GameUserSettings.ini`.
- Keep the settings under the `[GraceShield]` category.
- Restart the server after changing these values.
