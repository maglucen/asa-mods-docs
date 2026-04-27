# Troubleshooting

## Config changes are not applying

Check the following:

1. The config category name is correct.
2. The config entry names are spelled exactly as documented.
3. The server was restarted after editing the file.
4. The host did not overwrite `GameUserSettings.ini` after restart.
5. The mod is loaded by the server.

## The mod appears installed but does nothing

Confirm that the mod is present in the active server mod list, not only downloaded locally.

For mods with configurable behavior, also check whether the relevant option is disabled or left at a neutral/default value.

## Multiplayer behavior differs from single-player

Server authority can affect when configuration and replicated state become visible to clients. Test server-side behavior first, then verify what clients receive after joining or reconnecting.

## Reporting issues

When reporting a bug, include:

- mod name;
- mod version;
- single-player or dedicated server;
- map;
- relevant config section;
- steps to reproduce;
- screenshots or clips if useful.
