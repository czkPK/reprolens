from __future__ import annotations

import importlib.metadata as metadata
from pathlib import Path
from typing import Any

from .catalog import normalize_license
from .models import Dependency
from .parsers import discover_dependencies, load_license_overrides, parse_package_lock


COMMON_LICENSES = {
    "requests": "Apache-2.0",
    "numpy": "BSD-3-Clause",
    "pandas": "BSD-3-Clause",
    "scipy": "BSD-3-Clause",
    "flask": "BSD-3-Clause",
    "django": "BSD-3-Clause",
    "fastapi": "MIT",
    "click": "BSD-3-Clause",
    "pydantic": "MIT",
    "pytest": "MIT",
    "setuptools": "MIT",
    "pip": "MIT",
    "license-expression": "Apache-2.0",
    "scancode-toolkit": "Apache-2.0",
    "react": "MIT",
    "vue": "MIT",
    "typescript": "Apache-2.0",
    "lodash": "MIT",
    "axios": "MIT",
    "express": "MIT",
}


def _normalize_name(name: str) -> str:
    return name.lower().replace("_", "-")


def _override_value(overrides: dict[str, Any], name: str) -> str | None:
    for key, value in overrides.items():
        if key.startswith("_"):
            continue
        if _normalize_name(key) != _normalize_name(name):
            continue
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get("license") or value.get("spdx")
    return None


def _installed_license(name: str) -> str | None:
    try:
        package_metadata = metadata.metadata(name)
    except metadata.PackageNotFoundError:
        return None
    expression = package_metadata.get("License-Expression")
    if expression:
        return str(expression)
    classifiers = package_metadata.get_all("Classifier") or []
    for classifier in classifiers:
        if classifier.startswith("License ::"):
            tail = classifier.split("::")[-1].strip()
            if tail:
                return tail
    license_value = package_metadata.get("License")
    if license_value and len(str(license_value)) <= 120:
        return str(license_value)
    return None


def resolve_dependencies(root: Path) -> list[Dependency]:
    overrides = load_license_overrides(root)
    npm_lock = parse_package_lock(root / "package-lock.json")
    resolved: list[Dependency] = []

    for name, version, source in discover_dependencies(root):
        key = _normalize_name(name)
        license_value = _override_value(overrides, name)
        evidence = [f"manifest:{source}"]
        confidence = 0.95
        if license_value:
            evidence.append("override:licenses.json")
        elif key in npm_lock:
            license_value = npm_lock[key]
            evidence.append("metadata:package-lock.json")
            confidence = 0.9
        else:
            license_value = _installed_license(name)
            if license_value:
                evidence.append("metadata:python-distribution")
            elif key in COMMON_LICENSES:
                license_value = COMMON_LICENSES[key]
                evidence.append("catalog:common-packages")
                confidence = 0.75
        canonical = normalize_license(license_value)
        if canonical == "UNKNOWN":
            confidence = 0.2
            evidence.append("missing:explicit-license")
        resolved.append(
            Dependency(
                name=name,
                version=version,
                license_spdx=canonical,
                source=source,
                confidence=confidence,
                evidence=evidence,
            )
        )
    return resolved


def project_license_override(root: Path) -> str | None:
    overrides = load_license_overrides(root)
    value = overrides.get("_project_license")
    if isinstance(value, str):
        return normalize_license(value)
    return None
