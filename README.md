# OpenPrintTag Color Search

Simple Python script for searching the
[OpenPrintTag Database](https://github.com/OpenPrintTag/openprinttag-database)
by filament color and optional material type.

The script searches through all material YAML files and returns matching:

- manufacturers
- filament names
- material types
- color values
- web link to the filament (It's not added for all manufacturers)

---

## Features

- Search by HEX color
- Optional material filter (`PETG`, `PLA`, `ABS`, etc.)
- Reads directly from a local OpenPrintTag database
- No database server required


---

## Example Output
```text
python optd_color.py #363331ff

Hits för #363331ff with material PETG: 3

Found #363331ff: 3

Manufacturer:
- Atomic Filament
- Prusament
- SIDDAMENT
Details:
- Atomic Filament | PETG | Translucent Smoke Black PETG PRO | #363331ff
  openprinttag-database/data/materials/atomic-filament/atomic-filament-translucent-smoke-black-petg-pro.yaml
  URL: https://atomicfilament.com/products/translucent-smoke-black-petg-pro
- Prusament | PETG | PETG V0 Jet Black | #363331ff
  openprinttag-database/data/materials/prusament/prusament-petg-v0-jet-black.yaml
  URL: https://www.prusa3d.com/product/prusament-petg-v0-jet-black-1kg/
- SIDDAMENT | PLA | Black HTPLA | #363331ff
  openprinttag-database/data/materials/siddament/siddament-black-htpla.yaml
  URL: https://siddament.com.au/products/black-htpla
```
---
## Installation
```bash
git clone https://github.com/gertlind/optd-color.git
cd optd-color
git clone https://github.com/OpenPrintTag/openprinttag-database.git
```

### Create virtual environment
- python3 -m venv .venv
- Activate the virtual environment:
  - source .venv/bin/activate
- Install requirements
  - pip install -r requirements.txt

### Run the script
```bash
python optd_color.py 363331ff
or
python optd_color.py #363331ff
```
This gives the output as Example Output.

## Disclamer
```text
Not all vendors have a link to the filament in the database
Some vendors have a link to a picture of the product (I have left that out).

I have browsed around and looked on several diffrent filaments that comes up for the same code, its very hard to determine if it exactly the same color from out of the pictures.
To me it feels like additions to the database is done automatic and a lot of filament is added by "looks like".

The best way to find out is to browse to vendor and look if they have added the correct color code (#363331ff)
Take it for what its worth.
```



