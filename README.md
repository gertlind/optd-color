# OpenPrintTag Color Search

Simple Python script for searching the
[OpenPrintTag Database](https://github.com/OpenPrintTag/openprinttag-database)
by filament color and optional material type.

The script searches through all material YAML files and returns matching:

- manufacturers
- filament names
- material types
- color values
- source YAML files

---

## Features

- Search by HEX color
- Optional material filter (`PETG`, `PLA`, `ABS`, etc.)
- Reads directly from a local OpenPrintTag database
- No database server required
- Works locally with YAML files

---

## Example Output

```text
Hits för #363331ff med material PETG: 2

Manufacturer:
- Atomic Filament
- Prusament

Details:
- Atomic Filament | PETG | Translucent Smoke Black PETG PRO | #363331ff
  openprinttag-database/data/materials/atomic-filament/atomic-filament-translucent-smoke-black-petg-pro.yaml

- Prusament | PETG | PETG V0 Jet Black | #363331ff
  openprinttag-database/data/materials/prusament/prusament-petg-v0-jet-black.yaml

---

## Installation

- git clone https://github.com/gertlind/optd-color.git
- cd optd-color
- git clone https://github.com/OpenPrintTag/openprinttag-database.git

