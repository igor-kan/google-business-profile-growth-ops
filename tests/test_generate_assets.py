from pathlib import Path

from src.generate_assets import generate


def test_generate_assets(tmp_path: Path) -> None:
    csv_path = tmp_path / "businesses.csv"
    csv_path.write_text(
        "business_name,category,city,value_prop,phone\n"
        "Bright Plumbing,Plumbing,Toronto,fast emergency service,+1-647-555-0100\n"
    )
    result = generate(csv_path, tmp_path / "out")
    assert result.business_count == 1
    assert (tmp_path / "out" / "bright-plumbing" / "gbp_growth_pack.md").exists()
