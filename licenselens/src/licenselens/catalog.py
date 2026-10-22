from __future__ import annotations

from .models import LicenseInfo


_ALIASES = {
    "mit license": "MIT",
    "mit": "MIT",
    "apache 2.0": "Apache-2.0",
    "apache-2.0": "Apache-2.0",
    "apache2": "Apache-2.0",
    "bsd-2-clause": "BSD-2-Clause",
    "bsd 2-clause": "BSD-2-Clause",
    "bsd-3-clause": "BSD-3-Clause",
    "bsd 3-clause": "BSD-3-Clause",
    "bsd license": "BSD-3-Clause",
    "apache software license": "Apache-2.0",
    "mpl-2.0": "MPL-2.0",
    "mpl 2.0": "MPL-2.0",
    "lgpl-2.1": "LGPL-2.1-only",
    "lgpl-3.0": "LGPL-3.0-only",
    "lgplv3": "LGPL-3.0-only",
    "gpl-2.0": "GPL-2.0-only",
    "gpl-3.0": "GPL-3.0-only",
    "gplv3": "GPL-3.0-only",
    "agpl-3.0": "AGPL-3.0-only",
    "agplv3": "AGPL-3.0-only",
    "unlicense": "Unlicense",
    "cc0": "CC0-1.0",
    "cc0-1.0": "CC0-1.0",
    "proprietary": "Proprietary",
    "unknown": "UNKNOWN",
}


_LICENSES = {
    "MIT": LicenseInfo("MIT", "MIT License", ("include-copyright", "include-license"), notice_required=True),
    "Apache-2.0": LicenseInfo(
        "Apache-2.0",
        "Apache License 2.0",
        ("include-license", "include-notice", "state-changes", "patent-grant"),
        notice_required=True,
    ),
    "BSD-2-Clause": LicenseInfo("BSD-2-Clause", "BSD 2-Clause License", ("include-copyright", "include-license"), notice_required=True),
    "BSD-3-Clause": LicenseInfo(
        "BSD-3-Clause",
        "BSD 3-Clause License",
        ("include-copyright", "include-license", "no-endorsement"),
        notice_required=True,
    ),
    "MPL-2.0": LicenseInfo(
        "MPL-2.0",
        "Mozilla Public License 2.0",
        ("file-level-copyleft", "include-license", "state-changes"),
        source_disclosure=True,
        notice_required=True,
    ),
    "LGPL-2.1-only": LicenseInfo(
        "LGPL-2.1-only",
        "GNU Lesser General Public License 2.1",
        ("weak-copyleft", "include-license", "allow-relinking"),
        source_disclosure=True,
        notice_required=True,
    ),
    "LGPL-3.0-only": LicenseInfo(
        "LGPL-3.0-only",
        "GNU Lesser General Public License 3.0",
        ("weak-copyleft", "include-license", "allow-relinking"),
        source_disclosure=True,
        notice_required=True,
    ),
    "GPL-2.0-only": LicenseInfo(
        "GPL-2.0-only",
        "GNU General Public License 2.0",
        ("strong-copyleft", "include-license", "provide-source"),
        source_disclosure=True,
        notice_required=True,
    ),
    "GPL-3.0-only": LicenseInfo(
        "GPL-3.0-only",
        "GNU General Public License 3.0",
        ("strong-copyleft", "include-license", "provide-source"),
        source_disclosure=True,
        notice_required=True,
    ),
    "AGPL-3.0-only": LicenseInfo(
        "AGPL-3.0-only",
        "GNU Affero General Public License 3.0",
        ("strong-copyleft", "network-copyleft", "include-license", "provide-source"),
        source_disclosure=True,
        network_copyleft=True,
        notice_required=True,
    ),
    "Unlicense": LicenseInfo("Unlicense", "The Unlicense", ()),
    "CC0-1.0": LicenseInfo("CC0-1.0", "Creative Commons Zero 1.0", ()),
    "Proprietary": LicenseInfo("Proprietary", "Proprietary or custom license", ("manual-review",), unknown=True, proprietary=True),
    "UNKNOWN": LicenseInfo("UNKNOWN", "Unknown license", ("manual-review",), unknown=True),
}


def normalize_license(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    cleaned = " ".join(str(value).strip().lower().replace("_", "-").split())
    if cleaned in _ALIASES:
        return _ALIASES[cleaned]
    for prefix, canonical in (
        ("apache", "Apache-2.0"),
        ("bsd", "BSD-3-Clause"),
        ("bsd-2", "BSD-2-Clause"),
        ("agpl", "AGPL-3.0-only"),
        ("lgpl", "LGPL-3.0-only"),
        ("gpl", "GPL-3.0-only"),
        ("mpl", "MPL-2.0"),
        ("mit", "MIT"),
    ):
        if cleaned.startswith(prefix):
            return canonical
    return "UNKNOWN"


def get_license(value: str | None) -> LicenseInfo:
    canonical = normalize_license(value)
    return _LICENSES.get(canonical, _LICENSES["UNKNOWN"])

