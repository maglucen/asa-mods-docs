# Golem Nemesis Configuration

Add the following section to `GameUserSettings.ini`:

```ini
[GolemNemesis]
DamagePercentage=100.0
bUseDamageTypeDetection=true
bAllowToolDamageTypes=true
DinoWhitelist=
DinoBlacklist=
DinoParentWhitelist=
DinoParentBlacklist=
```

## Settings

### `DamagePercentage`

Controls how much normal damage valid attackers deal to Rock Golems and compatible child classes.

- `100.0` = normal damage
- `10.0` = minimum allowed value
- `50.0` = half damage
- `200.0` = double damage
- values below `10.0` are clamped to `10.0`

### `bUseDamageTypeDetection`

Controls which base set of attackers is allowed to deal normal damage.

- `true` = uses supported `DamageType` detection
- `false` = ignores `DamageType` detection and uses only the classic hardcoded dino classes

When this is set to `false`, the default allowed dinos are:

- `Ankylo_Character_BP_C`
- `Doed_Character_BP_C`
- `Dunkle_Character_BP_C`

### `bAllowToolDamageTypes`

Only used when `bUseDamageTypeDetection=true`.

- `true` = supported tool-based damage types also count
- `false` = tool-based damage types are ignored

This setting is ignored when `bUseDamageTypeDetection=false`.

### `DinoWhitelist`

Comma-separated list of exact dino classes.

These entries are normalized and compared as exact class matches.

Accepted formats:

- `Doed_Character_BP_C`
- `/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP_C`
- `Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP'`
- `BlueprintGeneratedClass'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP_C'`

All of the examples above resolve to the same exact dino class.

Example:

```ini
DinoWhitelist=Mantis_Character_BP_C,Doed_Character_BP_Aberrant_C
```

### `DinoBlacklist`

Comma-separated list of exact dino classes.

These entries use the same accepted formats as `DinoWhitelist`.

Exact blacklist entries have the highest priority and always win over:

- exact whitelist
- parent whitelist
- parent blacklist
- default detection
- `DamageType` detection

Example:

```ini
DinoBlacklist=Dunkle_Character_BP_C
```

### `DinoParentWhitelist`

Comma-separated list of parent dino classes.

Any child class of an entry in this list is also allowed.

Accepted formats:

- `/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP_C`
- `Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP'`
- `BlueprintGeneratedClass'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP_C'`

Short names such as `Doed_Character_BP_C` should be used in the direct lists, not in the parent lists.

Example:

```ini
DinoParentWhitelist=Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP'
```

### `DinoParentBlacklist`

Comma-separated list of parent dino classes.

Any child class of an entry in this list is also excluded.

These entries use the same accepted formats as `DinoParentWhitelist`.

Example:

```ini
DinoParentBlacklist=Blueprint'/Game/PrimalEarth/Dinos/Dunkleosteus/Dunkle_Character_BP.Dunkle_Character_BP'
```

## Priority Rules

Final behavior follows this priority:

1. exact blacklist
2. exact whitelist
3. parent blacklist
4. parent whitelist
5. if no list applies, the mod uses the active base detection mode

Important consequences:

- direct lists have priority over parent lists
- blacklist has priority over whitelist at the same level
- an exact whitelist entry can override a parent blacklist entry
- an exact blacklist entry cannot be overridden by any whitelist

Equivalent order:

```text
Exact Blacklist > Exact Whitelist > Parent Blacklist > Parent Whitelist > Base Detection
```

## Detection Modes

### Mode 1: `bUseDamageTypeDetection=false`

Uses only the default hardcoded dinos as the base set:

- `Ankylo_Character_BP_C`
- `Doed_Character_BP_C`
- `Dunkle_Character_BP_C`

In this mode:

- `bAllowToolDamageTypes` is ignored
- `DinoWhitelist` adds extra dinos
- `DinoParentWhitelist` adds extra dinos through inheritance
- `DinoBlacklist` removes dinos, including the default 3
- `DinoParentBlacklist` removes dinos, including children of matching parent classes

Important:

`DinoWhitelist` and `DinoParentWhitelist` do not replace the default 3 dinos. They only add to them.  
If you want to remove one of the default 3 dinos, you must explicitly add it to `DinoBlacklist` or `DinoParentBlacklist`.

### Mode 2: `bUseDamageTypeDetection=true`

Uses supported `DamageType` detection as the base set.

In this mode:

- natural anti-rock damage types can be allowed
- tool-based damage types can also be allowed if `bAllowToolDamageTypes=true`
- `DinoWhitelist` can add specific dinos even if their `DamageType` would not normally qualify
- `DinoParentWhitelist` can add child classes through a matching parent class
- `DinoBlacklist` can remove specific dinos even if their `DamageType` would normally qualify
- `DinoParentBlacklist` can remove child classes through a matching parent class

When a hit is valid through `DamageType` detection, the final result is still filtered by the configured lists.

In practice:

1. exact blacklist is checked first
2. then parent blacklist
3. if blocked by a parent blacklist, an exact whitelist can still allow that exact dino
4. if nothing blocks it, the `DamageType` result is used

This means `DamageType` detection is the base result, but the config lists still have the final word.

## Example Configurations

### Default behavior

```ini
[GolemNemesis]
DamagePercentage=100.0
bUseDamageTypeDetection=true
bAllowToolDamageTypes=true
DinoWhitelist=
DinoBlacklist=
DinoParentWhitelist=
DinoParentBlacklist=
```

### Classic behavior with one extra dino and one removed default dino

```ini
[GolemNemesis]
DamagePercentage=100.0
bUseDamageTypeDetection=false
bAllowToolDamageTypes=true
DinoWhitelist=Mantis_Character_BP_C
DinoBlacklist=Dunkle_Character_BP_C
DinoParentWhitelist=
DinoParentBlacklist=
```

Result:

- `Ankylo_Character_BP_C` is allowed
- `Doed_Character_BP_C` is allowed
- `Dunkle_Character_BP_C` is not allowed
- `Mantis_Character_BP_C` is allowed
- `bAllowToolDamageTypes` is ignored in this mode

### Global detection with a blacklist

```ini
[GolemNemesis]
DamagePercentage=125.0
bUseDamageTypeDetection=true
bAllowToolDamageTypes=true
DinoWhitelist=
DinoBlacklist=Dunkle_Character_BP_C
DinoParentWhitelist=
DinoParentBlacklist=
```

Result:

- valid attackers detected by supported `DamageType` deal `125%` normal damage
- tool-based damage types are enabled
- `Dunkle_Character_BP_C` is still excluded because blacklist has priority

### Exact override over parent blacklist

```ini
[GolemNemesis]
DamagePercentage=100.0
bUseDamageTypeDetection=true
bAllowToolDamageTypes=true
DinoWhitelist=Doed_Character_BP_C
DinoBlacklist=
DinoParentWhitelist=
DinoParentBlacklist=Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP'
```

Result:

- child classes of `Doed_Character_BP` are blocked by the parent blacklist
- the exact class `Doed_Character_BP_C` is still allowed because exact whitelist has priority over parent blacklist

## Editing Notes

- Stop the server before editing config values.
- Save the file and restart the server after making changes.
- Keep the config under the `[GolemNemesis]` section.
