from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from repolens.local_semantic import MODEL_PATH, build_model


def main() -> int:
    training_path = ROOT / "src" / "repolens" / "data" / "semantic_training.json"
    training = json.loads(training_path.read_text(encoding="utf-8"))
    model = build_model(training)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {MODEL_PATH}")
    print(f"Criteria: {len(model['criteria'])}; features: {model['dimension']}; training hash: {model['training_data_sha256'][:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
