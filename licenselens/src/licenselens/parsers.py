from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any


_REQ_RE = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?\s*(.*)$")


def _clean_requirement(line: str) -> tuple[str, str | None] | None:
    line = line.split("#", 1)[0].strip()
    if not line or line.startswith(("-", "git+", "http://", "https://")):
        return None
    if ";" in line:
        line = line.split(";", 1)[0].strip()
    match = _REQ_RE.match(line)
    if not match:
        return None
    name = match.group(1)
    version = match.group(2).strip() or None
    if version:
        version = version.lstrip("=<>!~").strip() or None
    return name, version


def parse_requirements(path: Path) -> list[tuple[str, str | None]]:
    dependencies: list[tuple[str, str | None]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = _clean_requirement(line)
        if parsed:
            dependencies.append(parsed)
    return dependencies


def parse_pyproject(path: Path) -> list[tuple[str, str | None]]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    dependencies: list[tuple[str, str | None]] = []
    project = data.get("project", {})
    for item in project.get("dependencies", []) or []:
        parsed = _clean_requirement(str(item))
        if parsed:
            dependencies.append(parsed)
    poetry = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    if isinstance(poetry, dict):
        for name, spec in poetry.items():
            if name.lower() == "python":
                continue
            version = spec.get("version") if isinstance(spec, dict) else str(spec)
            dependencies.append((name, version))
    return dependencies


def parse_package_json(path: Path) -> list[tuple[str, str | None]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    dependencies: list[tuple[str, str | None]] = []
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        for name, version in (data.get(section) or {}).items():
            dependencies.append((name, str(version)))
    return dependencies


def parse_package_lock(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    packages = data.get("packages")
    if isinstance(packages, dict):
        for key, value in packages.items():
            if not key or not isinstance(value, dict):
                continue
            name = key.rsplit("node_modules/", 1)[-1]
            license_value = value.get("license")
            if name and license_value:
                result[name.lower()] = str(license_value)
    for name, value in (data.get("dependencies") or {}).items():
        if isinstance(value, dict) and value.get("license"):
            result.setdefault(name.lower(), str(value["license"]))
    return result


def load_license_overrides(root: Path) -> dict[str, Any]:
    path = root / "licenses.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("licenses.json must contain a JSON object")
    return data


def discover_dependencies(root: Path) -> list[tuple[str, str | None, str]]:
    seen: set[str] = set()
    result: list[tuple[str, str | None, str]] = []
    candidates = [
        (root / "requirements.txt", "requirements.txt", parse_requirements),
        (root / "pyproject.toml", "pyproject.toml", parse_pyproject),
        (root / "package.json", "package.json", parse_package_json),
    ]
    for path, label, parser in candidates:
        if not path.exists():
            continue
        for name, version in parser(path):
            key = name.lower().replace("_", "-")
            if key not in seen:
                seen.add(key)
                result.append((name, version, label))
    return result

