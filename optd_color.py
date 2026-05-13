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
    for path in BRANDS_DIR.glob("*.yaml"):
        data = load_yaml(path)
        slug = data.get("slug") or path.stem
        brands[slug] = data.get("name", slug)
    return brands

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("color", help="Hex-färg, t.ex. 363331 eller '#363331ff'")
    parser.add_argument("--material", help="Valfritt materialfilter, t.ex. PETG, PLA, ABS")
    args = parser.parse_args()

    wanted_color = norm_hex(args.color)
    wanted_material = norm_text(args.material)

    brands = load_brands()
    matches = []

    for path in MATERIALS_DIR.glob("*/*.yaml"):
        data = load_yaml(path)

        color = norm_hex(data.get("primary_color", {}).get("color_rgba"))
        material = norm_text(data.get("type"))

        if color != wanted_color:
            continue

        if wanted_material and material != wanted_material:
            continue

        brand_slug = data.get("brand", {}).get("slug", path.parent.name)
        brand_name = brands.get(brand_slug, brand_slug)

        matches.append({
            "brand": brand_name,
            "name": data.get("name", ""),
            "type": data.get("type", ""),
            "color": color,
            "file": str(path),
            "url": (
                    data.get("product_url")
                    or data.get("url")
                    or data.get("website")
                    or ""
            ),
        })

    if not matches:
        if wanted_material:
            print(f"Inga träffar för {wanted_color} med material {args.material}")
        else:
            print(f"Inga träffar för {wanted_color}")
        return

    if wanted_material:
        print(f"Träffar för {wanted_color} med material {args.material}: {len(matches)}\n")
    else:
        print(f"Träffar för {wanted_color}: {len(matches)}\n")

    print("Tillverkare:")
    for brand in sorted(set(m["brand"] for m in matches)):
        print(f"- {brand}")

    print("\nDetaljer:")
    for m in sorted(matches, key=lambda x: (x["brand"], x["name"])):
        print(f"- {m['brand']} | {m['type']} | {m['name']} | {m['color']}")
        print(f"  {m['file']}")
        if m["url"]:
            print(f"  URL: {m['url']}")


if __name__ == "__main__":
    main()
