from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    cases_path = base / "benchmark" / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    by_name = {item["name"]: item for item in cases}
    labels_dir = base / "benchmark" / "labels"
    for path in sorted(labels_dir.glob("*.json")):
        label = json.loads(path.read_text(encoding="utf-8"))
        name = label["repo"]
        if name not in by_name:
            print(f"skip {name}: no matching case")
            continue
        by_name[name]["expected"] = {
            item["criterion_id"]: item["expected_status"] for item in label["criteria"]
        }
        by_name[name]["label_file"] = path.relative_to(base).as_posix()
        by_name[name]["project_type"] = label.get("project_type")
        print(f"merged {name}: {len(label['criteria'])} labels")
    cases_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
