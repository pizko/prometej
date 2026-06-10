from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "cities.json"


def slugify(value: str) -> str:
    letters = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z",
        "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
        "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    text = "".join(letters.get(ch, ch) for ch in value.lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "city"


def read_rows(path: Path) -> list[dict[str, str]]:
    raw = path.read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;	")
    reader = csv.DictReader(raw.splitlines(), dialect=dialect)
    rows = []
    for row in reader:
        cleaned = {str(key).strip(): (value or "").strip() for key, value in row.items() if key}
        if cleaned.get("city"):
            rows.append(cleaned)
    return rows


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_cities_csv.py path/to/cities.csv")

    rows = read_rows(Path(sys.argv[1]))
    items = []
    seen_slugs = set()

    for row in rows:
        city = row["city"]
        slug = row.get("slug") or slugify(city)
        original_slug = slug
        counter = 2
        while slug in seen_slugs:
            slug = f"{original_slug}-{counter}"
            counter += 1
        seen_slugs.add(slug)

        item = {
            "slug": slug,
            "city": city,
        }
        for field in ("region", "city_prepositional", "title", "description", "hero_intro"):
            if row.get(field):
                item[field] = row[field]
        items.append(item)

    OUTPUT_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Импортировано городов: {len(items)}")
    print(f"Файл: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
