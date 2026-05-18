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

    # If RGB change to RGBA with ff
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
        description="Search in OpenPrintTag database for color, material and/or brand"
    )

    parser.add_argument(
        "color",
        nargs="?",
        help="Choosable HEX-color, t.ex. 363331 or '#363331ff'",
    )

    parser.add_argument(
        "--material",
        help="Choosable material filter, ex. PETG, PLA, ABS...",
    )

    parser.add_argument(
        "--brand",
        "--manufacturer",
        dest="brand",
        help="Choosable manufacturer, ex. bambulab, prusament, atomic....",
    )

    args = parser.parse_args()

    wanted_color = norm_hex(args.color) if args.color else ""
    wanted_material = norm_text(args.material)
    wanted_brand = norm_text(args.brand)

    if not wanted_color and not wanted_material and not wanted_brand:
        print("Give minimum one search: color, --material eller --brand")
        print("")
        print("Exampel:")
        print("  python3 optd_color.py 363331")
        print("  python3 optd_color.py 363331 --material PETG")
        print("  python3 optd_color.py --brand bambulab")
        print("  python3 optd_color.py --brand bambulab --material PETG")
        return

    brands = load_brands()
    matches = []

    if not MATERIALS_DIR.exists():
        print(f"Cannot find the database: {MATERIALS_DIR}")
        print("Check that the database folder exists")
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

        # Filter: brand
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
            "url": (data.get("product_url")
                    or data.get("website")
                    or data.get("url")
                    or "" ),
            "photo_url": (
                data.get("photos", [{}])[0].get("url")
                if data.get("photos")
                else ""
            ),
        })

    if not matches:
        print("Nothing found.")
        return

    # Header
    filters = []

    if wanted_color:
        filters.append(f"color {wanted_color}")

    if wanted_material:
        filters.append(f"material {args.material}")

    if wanted_brand:
        filters.append(f"manufacturer {args.brand}")

    print(f"Hits for {', '.join(filters)}: {len(matches)}\n")

    print("Manufactorer:")
    for brand in sorted(set(m["brand"] for m in matches)):
        print(f"- {brand}")

    print("\nDetails:")
    for m in sorted(matches, key=lambda x: (x["brand"], x["type"], x["name"])):
        print(f"- {m['brand']} | {m['type']} | {m['name']} | {m['color']}")
        #print(f"  {m['file']}")
        if m["url"]:
            print(f"  URL: {m['url']}")
        if m["photo_url"]:
            print(f"  Photo: {m['photo_url']}")

if __name__ == "__main__":
    main()
