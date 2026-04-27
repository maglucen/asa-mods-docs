# GameUserSettings.ini Location

Most configuration values for these mods are read from `GameUserSettings.ini`.

## Common server path

The exact path depends on the host, but it is usually inside the server saved config directory:

```ini
ShooterGame/Saved/Config/WindowsServer/GameUserSettings.ini
```

Some hosts expose this file through a control panel instead of direct file access.

## Single-player path

For local/single-player setups, the file is usually under the local ARK: Survival Ascended saved config directory.

## Editing notes

- Stop the server before editing config values.
- Keep each mod config under its own category header.
- Do not duplicate the same config category multiple times unless you know how your host merges config files.
- Restart the server after saving changes.
