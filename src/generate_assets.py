from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BusinessRow:
    business_name: str
    category: str
    city: str
    value_prop: str
    phone: str


@dataclass
class BuildResult:
    output_dir: Path
    business_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Google Business Profile growth assets")
    parser.add_argument("--input", required=True, help="Input CSV path")
    parser.add_argument("--output", default="out", help="Output directory")
    return parser.parse_args()


def _load_rows(path: Path) -> list[BusinessRow]:
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")

    rows: list[BusinessRow] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"business_name", "category", "city", "value_prop", "phone"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV headers: {sorted(missing)}")
        for raw in reader:
            rows.append(
                BusinessRow(
                    business_name=str(raw["business_name"]).strip(),
                    category=str(raw["category"]).strip(),
                    city=str(raw["city"]).strip(),
                    value_prop=str(raw["value_prop"]).strip(),
                    phone=str(raw["phone"]).strip(),
                )
            )
    return rows


def _slug(text: str) -> str:
    return "-".join(text.lower().replace("&", "and").split())


def _build_profile_pack(row: BusinessRow) -> str:
    return (
        f"# GBP Growth Pack - {row.business_name}\n\n"
        f"## Core profile description\n"
        f"{row.business_name} is a {row.category} service in {row.city}. "
        f"We focus on {row.value_prop}. Call us at {row.phone} to get started.\n\n"
        f"## Services bullets\n"
        f"- {row.category} delivery with clear timelines\n"
        f"- Transparent pricing and communication\n"
        f"- Local support for {row.city} customers\n\n"
        f"## Weekly posting prompts\n"
        f"1. Before/after customer story\n"
        f"2. FAQ + short answer\n"
        f"3. Local seasonal offer\n"
        f"4. Team/process spotlight\n\n"
        f"## Q&A seed list\n"
        f"- What areas in {row.city} do you serve?\n"
        f"- How quickly can we book?\n"
        f"- What is included in your base package?\n"
    )


def generate(input_csv: Path, output_dir: Path) -> BuildResult:
    rows = _load_rows(input_csv)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = output_dir / "manifest.csv"
    with open(manifest_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["business_name", "pack_path"])

        for row in rows:
            slug = _slug(row.business_name)
            business_dir = output_dir / slug
            business_dir.mkdir(parents=True, exist_ok=True)
            pack_path = business_dir / "gbp_growth_pack.md"
            pack_path.write_text(_build_profile_pack(row), encoding="utf-8")
            writer.writerow([row.business_name, str(pack_path)])

    return BuildResult(output_dir=output_dir, business_count=len(rows))


def main() -> None:
    args = parse_args()
    result = generate(Path(args.input), Path(args.output))
    print(f"Generated GBP packs for {result.business_count} businesses -> {result.output_dir}")


if __name__ == "__main__":
    main()
