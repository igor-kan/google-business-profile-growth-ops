# google-business-profile-growth-ops

Generate structured Google Business Profile optimization packs from CSV inputs.

## What it does
- Reads business profile inputs from CSV
- Generates markdown packs with profile description, service bullets, weekly post prompts, and Q&A seeds
- Exports a manifest for delivery workflows

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_assets.py --input examples/businesses.csv --output out
```

## Outputs
- `out/<business-slug>/gbp_growth_pack.md`
- `out/manifest.csv`

## API/terms references
- Google Places Text Search: https://developers.google.com/maps/documentation/places/web-service/text-search
- Google Maps Platform Terms: https://cloud.google.com/maps-platform/terms/index-20180501
- Google Business Profile APIs: https://developers.google.com/my-business
