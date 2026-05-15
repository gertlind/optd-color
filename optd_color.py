#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

DATA_DIR = Path("openprinttag-database/data")
MATERIALS_DIR = DATA_DIR / "materials"
BRANDS_DIR = DATA_DIR / "brands"


def norm_hex(value):
    if not value:
        return ""

    value = str(value).strip().lower()

    if not value.startswith("#"):
        value = "#" + value

    # Om man anger RGB, gör om till RGBA med ff
    if len(value) == 7:
        value += "ff"

    return value


def norm_text(value):
    return str(value or "").strip().lower()


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_brands():
    brands = {}

    if not BRANDS_DIR.exists():
        return brands

    for path in BRANDS_DIR.glob("*.yaml"):
        data = load_yaml(path)
        slug = data.get("slug") or path.stem
        brands[slug] = data.get("name", slug)

    return brands


def main():
    parser = argparse.ArgumentParser(
        description="Sök i OpenPrintTag Database efter färg, material och/eller tillverkare"
    )

    parser.add_argument(
        "color",
        nargs="?",
        help="Valfri HEX-färg, t.ex. 363331 eller '#363331ff'",
    )

    parser.add_argument(
        "--material",
        help="Valfritt materialfilter, t.ex. PETG, PLA, ABS",
    )

    parser.add_argument(
        "--brand",
        "--manufacturer",
        dest="brand",
        help="Valfri tillverkare, t.ex. bambulab, prusament, atomic",
    )

    args = parser.parse_args()

    wanted_color = norm_hex(args.color) if args.color else ""
    wanted_material = norm_text(args.material)
    wanted_brand = norm_text(args.brand)

    if not wanted_color and not wanted_material and not wanted_brand:
        print("Ange minst en sökning: färg, --material eller --brand")
        print("")
        print("Exempel:")
        print("  python3 optd_color.py 363331")
        print("  python3 optd_color.py 363331 --material PETG")
        print("  python3 optd_color.py --brand bambulab")
        print("  python3 optd_color.py --brand bambulab --material PETG")
        return

    brands = load_brands()
    matches = []

    if not MATERIALS_DIR.exists():
        print(f"Hittar inte databasen: {MATERIALS_DIR}")
        print("Kontrollera att openprinttag-database ligger bredvid scriptet.")
        return

    for path in MATERIALS_DIR.glob("*/*.yaml"):
        data = load_yaml(path)

        color = norm_hex(data.get("primary_color", {}).get("color_rgba"))
        material = norm_text(data.get("type"))

        brand_slug = data.get("brand", {}).get("slug", path.parent.name)
        brand_name = brands.get(brand_slug, brand_slug)

        # Filter: färg
        if wanted_color and color != wanted_color:
            continue

        # Filter: material
        if wanted_material and material != wanted_material:
            continue

        # Filter: tillverkare
        if wanted_brand:
            brand_search = f"{brand_slug} {brand_name}".lower()
            if wanted_brand not in brand_search:
                continue

        matches.append({
            "brand": brand_name,
            "brand_slug": brand_slug,
            "name": data.get("name", ""),
            "type": data.get("type", ""),
            "color": color,
            "file": str(path),
        })

    if not matches:
        print("Inga träffar.")
        return

    # Rubrik
    filters = []

    if wanted_color:
        filters.append(f"färg {wanted_color}")

    if wanted_material:
        filters.append(f"material {args.material}")

    if wanted_brand:
        filters.append(f"tillverkare {args.brand}")

    print(f"Träffar för {', '.join(filters)}: {len(matches)}\n")

    print("Tillverkare:")
    for brand in sorted(set(m["brand"] for m in matches)):
        print(f"- {brand}")

    print("\nDetaljer:")
    for m in sorted(matches, key=lambda x: (x["brand"], x["type"], x["name"])):
        print(f"- {m['brand']} | {m['type']} | {m['name']} | {m['color']}")
        print(f"  {m['file']}")

if __name__ == "__main__":
    main()
