from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_DATA_SOURCE_ID = "353c9091-cfac-8039-af71-000b53574bd0"
DEFAULT_NOTION_VERSION = "2025-09-03"
DEFAULT_OUTPUT_PATH = Path(__file__).with_name("tracker.md")

GROUP_ORDER = [
    "Official Tameables - The Island",
    "Official Tameables - Scorched Earth",
    "Official Tameables - Aberration / Aberration Ascended",
    "Official Tameables - Extinction",
    "Official Tameables - Ragnarok",
    "Official Tameables - Lost Colony",
    "Official DLC / Multi-Map Tameables - Fantastic Tames",
    "Official DLC / Multi-Map Tameables - Additions Ascended / Official ASA Additions",
    "Official Global / Multi-Map Tameables",
    "Official Tameables - Aberrant Variants",
]

STATE_BADGES = {
    "Public": "![Public](https://img.shields.io/badge/Public-2ea44f)",
    "Internal": "![Internal](https://img.shields.io/badge/Internal-d29922)",
    "Planned": "![Planned](https://img.shields.io/badge/Planned-6e7781)",
}

TRACKING_COLUMNS = [
    "Idle",
    "Vocal",
    "MoveGround",
    "MoveFly",
    "MoveWater",
    "Eat",
    "LayEgg",
    "Cuddle",
]

FINAL_NOTES_SECTION = [
    "## Notes",
    "",
    "- This tracker intentionally focuses on tameable creatures that can realistically end up in a player's base and are relevant to Hush Tames.",
    "- Untameables, bosses, temporary/special-purpose summons, and announced-but-not-released creatures are intentionally excluded.",
    "- The tracker is grouped by official map or official DLC/source so it is easier to maintain alongside the data table.",
    "- If a creature later needs more granular tracking, additional sound columns or notes can be added without changing the overall tracker structure.",
]


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def normalize_data_source_id(value: str) -> str:
    normalized = value.strip()
    if normalized.startswith("collection://"):
        normalized = normalized.removeprefix("collection://")
    return normalized


def notion_request(
    method: str,
    path: str,
    token: str,
    notion_version: str,
    payload: dict | None = None,
) -> dict:
    url = f"https://api.notion.com{path}"
    body = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": notion_version,
        "Content-Type": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API error {error.code}: {details}") from error


def query_all_rows(data_source_id: str, token: str, notion_version: str) -> list[dict]:
    rows: list[dict] = []
    next_cursor: str | None = None
    while True:
        payload: dict = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        response = notion_request(
            "POST",
            f"/v1/data_sources/{data_source_id}/query",
            token,
            notion_version,
            payload,
        )
        rows.extend(response.get("results", []))
        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")
        if not next_cursor:
            break
    return rows


def rich_text_to_plain(items: list[dict] | None) -> str:
    if not items:
        return ""
    parts: list[str] = []
    for item in items:
        plain_text = item.get("plain_text")
        if plain_text is not None:
            parts.append(plain_text)
    return "".join(parts).strip()


def property_to_plain(property_value: dict) -> str:
    property_type = property_value.get("type")
    if property_type == "title":
        return rich_text_to_plain(property_value.get("title"))
    if property_type == "rich_text":
        return rich_text_to_plain(property_value.get("rich_text"))
    if property_type == "select":
        option = property_value.get("select")
        return option.get("name", "") if option else ""
    if property_type == "status":
        option = property_value.get("status")
        return option.get("name", "") if option else ""
    if property_type == "checkbox":
        return "Yes" if property_value.get("checkbox") else "No"
    if property_type == "formula":
        formula = property_value.get("formula", {})
        formula_type = formula.get("type")
        if formula_type == "string":
            return formula.get("string", "") or ""
        if formula_type == "boolean":
            return "Yes" if formula.get("boolean") else "No"
        if formula_type == "number":
            value = formula.get("number")
            return "" if value is None else str(value)
    return ""


def page_to_row(page: dict) -> dict:
    properties = page.get("properties", {})
    row = {
        "Group": property_to_plain(properties["Group"]),
        "Name": property_to_plain(properties["Name"]),
        "Variant": property_to_plain(properties["Variant"]) or "Standard",
        "State": property_to_plain(properties["State"]) or "Planned",
        "DT": property_to_plain(properties["DT"]) or "No",
        "Notes": property_to_plain(properties["Notes"]),
    }
    for column in TRACKING_COLUMNS:
        row[column] = property_to_plain(properties[column]) or "No"
    return row


def group_sort_key(group_name: str) -> tuple[int, str]:
    try:
        return (GROUP_ORDER.index(group_name), group_name)
    except ValueError:
        return (len(GROUP_ORDER), group_name)


def variant_sort_key(variant: str) -> tuple[int, str]:
    if variant == "Standard":
        return (0, variant)
    return (1, variant)


def row_sort_key(row: dict) -> tuple[tuple[int, str], str, tuple[int, str]]:
    return (
        group_sort_key(row["Group"]),
        row["Name"],
        variant_sort_key(row["Variant"]),
    )


def state_badge(state: str) -> str:
    if state not in STATE_BADGES:
        raise ValueError(f"Unsupported state '{state}'")
    return STATE_BADGES[state]


def render_row(row: dict) -> str:
    values = [
        state_badge(row["State"]),
        row["Name"],
        row["Variant"],
        row["DT"],
        row["Idle"],
        row["Vocal"],
        row["MoveGround"],
        row["MoveFly"],
        row["MoveWater"],
        row["Eat"],
        row["LayEgg"],
        row["Cuddle"],
        row["Notes"],
    ]
    return f"| {' | '.join(values)} |"


def render_tracker(rows: list[dict]) -> str:
    rows_by_group: dict[str, list[dict]] = {}
    for row in sorted(rows, key=row_sort_key):
        rows_by_group.setdefault(row["Group"], []).append(row)

    ordered_groups = [group for group in GROUP_ORDER if group in rows_by_group]
    extra_groups = sorted(
        [group for group in rows_by_group if group not in GROUP_ORDER],
        key=lambda item: item.lower(),
    )
    sections: list[str] = [
        "# Shhhhh Hush Tames Tracker",
        "",
        "This tracker is used to monitor creature coverage for the Hush Tames data table.",
        "",
        "It is intentionally **practical** rather than asset-exhaustive:",
        "",
        "- `State` summarizes whether the creature is only planned, already in the internal data table, or already included in the current public release.",
        "- `DT` tracks whether the creature has been added to the internal data table.",
        "- Sound columns track whether that sound category has already been isolated for that creature.",
        "- This document is meant to be easy to maintain while still being useful to players.",
        "",
        "## Legend",
        "",
        "- `Public` = already included in the current public CurseForge release",
        "- `Internal` = already in the internal data table, not yet in the public CurseForge release",
        "- `Planned` = not added yet",
        "- `No` = not added yet",
        "- `Yes` = added / isolated",
        "- `N/A` = not applicable or not planned for that creature",
        "- `Partial` = partial / still needs review",
        "",
        "## State Rules",
        "",
        "- Use `Planned` when the creature is not yet in the internal data table.",
        "- Use `Internal` when the creature is already in the internal data table but not yet included in the current CurseForge release.",
        "- Use `Public` when the creature is already included in the current CurseForge release.",
        "",
        "## Tracking Columns",
        "",
        "- `State`",
        "- `DT`",
        "- `Idle`",
        "- `Vocal`",
        "- `MoveGround`",
        "- `MoveFly`",
        "- `MoveWater`",
        "- `Eat`",
        "- `LayEgg`",
        "- `Cuddle`",
    ]

    for group_name in ordered_groups + extra_groups:
        sections.extend(
            [
                "",
                f"## {group_name}",
                "",
                "| State | Creature | Variant | DT | Idle | Vocal | MoveGround | MoveFly | MoveWater | Eat | LayEgg | Cuddle | Notes |",
                "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        sections.extend(render_row(row) for row in rows_by_group[group_name])

    sections.extend(["", *FINAL_NOTES_SECTION, ""])
    return "\n".join(sections)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync tracker.md from the Notion Tracker data source.")
    parser.add_argument(
        "--data-source-id",
        default=os.environ.get("NOTION_TRACKER_DATA_SOURCE_ID", DEFAULT_DATA_SOURCE_ID),
        help="Notion data source ID. Defaults to NOTION_TRACKER_DATA_SOURCE_ID or the repo default.",
    )
    parser.add_argument(
        "--output",
        default=os.environ.get("TRACKER_OUTPUT_PATH", str(DEFAULT_OUTPUT_PATH)),
        help="Output markdown path. Defaults to tracker.md next to this script.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the generated markdown instead of writing the output file.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(Path(__file__).with_name(".env"))
    args = parse_args()
    token = os.environ.get("NOTION_TOKEN")
    notion_version = os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION)
    if not token:
        print("Missing NOTION_TOKEN. Add it to the environment or to .env.", file=sys.stderr)
        return 1

    data_source_id = normalize_data_source_id(args.data_source_id)
    rows = [page_to_row(page) for page in query_all_rows(data_source_id, token, notion_version)]
    markdown = render_tracker(rows)

    if args.stdout:
        sys.stdout.write(markdown)
        return 0

    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8", newline="\n")
    print(f"Wrote {len(rows)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
