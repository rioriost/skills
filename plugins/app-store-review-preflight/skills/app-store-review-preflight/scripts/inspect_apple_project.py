#!/usr/bin/env python3
"""Read-only evidence collector for Apple App Store preflight audits."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".svn",
    ".hg",
    ".build",
    "DerivedData",
    "build",
    "dist",
    "node_modules",
    ".next",
}

SOURCE_SUFFIXES = {
    ".swift",
    ".m",
    ".mm",
    ".h",
    ".hpp",
    ".c",
    ".cc",
    ".cpp",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".dart",
    ".kt",
}

DEPENDENCY_NAMES = {
    "Package.swift",
    "Package.resolved",
    "Podfile",
    "Podfile.lock",
    "Cartfile",
    "Cartfile.resolved",
}

RISK_PATTERNS: dict[str, tuple[str, ...]] = {
    "in_app_purchase": (r"\bStoreKit\b", r"Product\.products", r"SKPaymentQueue"),
    "sign_in_with_apple": (r"AuthenticationServices", r"ASAuthorizationAppleIDProvider"),
    "web_content": (r"\bWebKit\b", r"\bWKWebView\b", r"SFSafariViewController"),
    "notifications": (r"\bUserNotifications\b", r"UNUserNotificationCenter"),
    "location": (r"\bCoreLocation\b", r"CLLocationManager"),
    "camera_or_microphone": (r"\bAVFoundation\b", r"AVCaptureSession", r"AVAudioRecorder"),
    "photos": (r"\bPhotos\b", r"PHPhotoLibrary"),
    "contacts": (r"\bContacts\b", r"CNContactStore"),
    "calendars_or_reminders": (r"\bEventKit\b", r"EKEventStore"),
    "health": (r"\bHealthKit\b", r"HKHealthStore"),
    "home": (r"\bHomeKit\b", r"HMHomeManager"),
    "bluetooth": (r"\bCoreBluetooth\b", r"CBCentralManager", r"CBPeripheralManager"),
    "external_hardware": (r"\bExternalAccessory\b", r"EAAccessoryManager"),
    "login_item_or_background_helper": (r"\bServiceManagement\b", r"SMAppService", r"SMLoginItemSetEnabled"),
    "cloud": (r"\bCloudKit\b", r"CKContainer"),
    "networking": (r"URLSession", r"Network\.framework", r"\bNWConnection\b"),
    "tracking": (r"AppTrackingTransparency", r"ATTrackingManager", r"\bAdSupport\b"),
    "advertising": (r"GoogleMobileAds", r"GADBannerView", r"AdServices", r"SKAdNetwork"),
    "user_generated_content": (r"reportUser", r"blockUser", r"moderation", r"userGeneratedContent"),
    "ai_generated_content": (r"\bOpenAI\b", r"ChatGPT", r"generativeAI", r"GenerativeAI"),
}

COMPILED_PATTERNS = {
    name: [re.compile(pattern) for pattern in patterns]
    for name, patterns in RISK_PATTERNS.items()
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect read-only App Store review evidence from an Apple project and optional .app bundle."
    )
    parser.add_argument("--project", required=True, help="Project or repository root")
    parser.add_argument("--app", help="Optional built .app bundle")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--max-source-bytes",
        type=int,
        default=3_000_000,
        help="Skip static source scanning for individual files larger than this value",
    )
    return parser.parse_args()


def normalized(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalized(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalized(item) for item in value]
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_plist(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with path.open("rb") as handle:
            value = plistlib.load(handle)
        if not isinstance(value, dict):
            return None, "plist root is not a dictionary"
        return normalized(value), None
    except Exception as exc:  # Evidence collection must continue across malformed files.
        return None, str(exc)


def walk_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        base = Path(dirpath)
        files.extend(base / name for name in filenames)
    return files


def info_plist_summary(path: Path, root: Path) -> dict[str, Any]:
    data, error = read_plist(path)
    item: dict[str, Any] = {"path": rel(path, root)}
    if error:
        item["error"] = error
        return item
    assert data is not None
    usage = {
        key: value
        for key, value in data.items()
        if key.endswith("UsageDescription") or key == "NSUserTrackingUsageDescription"
    }
    item.update(
        {
            "bundle_identifier": data.get("CFBundleIdentifier"),
            "display_name": data.get("CFBundleDisplayName") or data.get("CFBundleName"),
            "version": data.get("CFBundleShortVersionString"),
            "build": data.get("CFBundleVersion"),
            "minimum_os": data.get("MinimumOSVersion") or data.get("LSMinimumSystemVersion"),
            "usage_descriptions": usage,
            "background_modes": data.get("UIBackgroundModes", []),
            "ats": data.get("NSAppTransportSecurity"),
            "url_types": data.get("CFBundleURLTypes", []),
            "document_types": data.get("CFBundleDocumentTypes", []),
        }
    )
    return item


def entitlement_summary(path: Path, root: Path) -> dict[str, Any]:
    data, error = read_plist(path)
    item: dict[str, Any] = {"path": rel(path, root)}
    if error:
        item["error"] = error
    else:
        item["values"] = data
    return item


def privacy_summary(path: Path, root: Path) -> dict[str, Any]:
    data, error = read_plist(path)
    item: dict[str, Any] = {"path": rel(path, root)}
    if error:
        item["error"] = error
        return item
    assert data is not None
    item.update(
        {
            "tracking": data.get("NSPrivacyTracking"),
            "tracking_domains": data.get("NSPrivacyTrackingDomains", []),
            "collected_data_types": data.get("NSPrivacyCollectedDataTypes", []),
            "accessed_api_types": data.get("NSPrivacyAccessedAPITypes", []),
        }
    )
    return item


def collect_json_values(value: Any, keys: set[str], output: list[Any]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys and item not in (None, ""):
                output.append(item)
            collect_json_values(item, keys, output)
    elif isinstance(value, list):
        for item in value:
            collect_json_values(item, keys, output)


def storekit_summary(path: Path, root: Path) -> dict[str, Any]:
    item: dict[str, Any] = {"path": rel(path, root)}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        item["error"] = str(exc)
        return item
    identifiers: list[Any] = []
    product_types: list[Any] = []
    collect_json_values(data, {"productID", "productId", "id"}, identifiers)
    collect_json_values(data, {"type", "productType"}, product_types)
    item["product_identifiers"] = sorted({str(value) for value in identifiers})
    item["product_types"] = sorted({str(value) for value in product_types})
    return item


def scan_risk_signals(files: list[Path], root: Path, max_bytes: int) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {name: [] for name in COMPILED_PATTERNS}
    for path in files:
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, patterns in COMPILED_PATTERNS.items():
            if len(hits[name]) >= 12:
                continue
            if any(pattern.search(text) for pattern in patterns):
                hits[name].append(rel(path, root))
    return {name: paths for name, paths in hits.items() if paths}


def parse_plist_bytes(raw: bytes) -> dict[str, Any] | None:
    for marker in (b"<?xml", b"bplist00"):
        start = raw.find(marker)
        if start >= 0:
            try:
                value = plistlib.loads(raw[start:])
                return normalized(value) if isinstance(value, dict) else None
            except Exception:
                pass
    return None


def run_command(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, capture_output=True, check=False, timeout=30)
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout.decode("utf-8", errors="replace").strip(),
            "stderr": result.stderr.decode("utf-8", errors="replace").strip(),
            "raw_stdout": result.stdout,
            "raw_stderr": result.stderr,
        }
    except Exception as exc:
        return {"command": command, "error": str(exc)}


def inspect_app_bundle(app: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"path": str(app), "exists": app.exists()}
    if not app.exists():
        return result
    info_candidates = [app / "Contents" / "Info.plist", app / "Info.plist"]
    info_path = next((path for path in info_candidates if path.is_file()), None)
    if info_path:
        data, error = read_plist(info_path)
        result["info_plist"] = {"path": str(info_path), "values": data, "error": error}

    codesign = shutil.which("codesign")
    if codesign:
        verify = run_command([codesign, "--verify", "--deep", "--strict", str(app)])
        verify.pop("raw_stdout", None)
        verify.pop("raw_stderr", None)
        result["codesign_verify"] = verify

        entitlements = run_command([codesign, "-d", "--entitlements", ":-", str(app)])
        parsed = parse_plist_bytes(entitlements.get("raw_stdout", b"")) or parse_plist_bytes(
            entitlements.get("raw_stderr", b"")
        )
        result["signed_entitlements"] = parsed
        result["signed_entitlements_command_returncode"] = entitlements.get("returncode")
        if entitlements.get("error"):
            result["signed_entitlements_error"] = entitlements["error"]
    else:
        result["codesign_unavailable"] = True
    return result


def build_observations(report: dict[str, Any]) -> list[dict[str, str]]:
    observations: list[dict[str, str]] = []
    if not report["info_plists"]:
        observations.append(
            {
                "level": "evidence_gap",
                "topic": "Info.plist",
                "message": "No source Info.plist was found; verify generated build settings or inspect a built app.",
            }
        )
    for info in report["info_plists"]:
        for key, value in info.get("usage_descriptions", {}).items():
            if not isinstance(value, str) or not value.strip():
                observations.append(
                    {
                        "level": "warning",
                        "topic": key,
                        "message": f"{info['path']} contains an empty purpose string.",
                    }
                )
    if "tracking" in report["risk_signals"] and not any(
        info.get("usage_descriptions", {}).get("NSUserTrackingUsageDescription")
        for info in report["info_plists"]
    ):
        observations.append(
            {
                "level": "evidence_gap",
                "topic": "Tracking",
                "message": "Tracking-related source was detected but no NSUserTrackingUsageDescription was found in source plists.",
            }
        )
    if "in_app_purchase" in report["risk_signals"] and not report["storekit_configurations"]:
        observations.append(
            {
                "level": "evidence_gap",
                "topic": "In-App Purchase",
                "message": "StoreKit usage was detected without a local .storekit configuration; verify product IDs in code and App Store Connect.",
            }
        )
    app_bundle = report.get("app_bundle")
    if app_bundle and app_bundle.get("exists"):
        verify = app_bundle.get("codesign_verify", {})
        if verify.get("returncode") not in (None, 0):
            observations.append(
                {
                    "level": "warning",
                    "topic": "Code signature",
                    "message": "codesign verification failed for the supplied app bundle.",
                }
            )
    return observations


def collect_report(project: Path, app: Path | None, max_source_bytes: int) -> dict[str, Any]:
    files = walk_files(project)
    info_plists = [path for path in files if path.name == "Info.plist"]
    entitlements = [path for path in files if path.suffix == ".entitlements"]
    privacy = [path for path in files if path.suffix == ".xcprivacy"]
    storekit = [path for path in files if path.suffix == ".storekit"]
    dependency_files = [path for path in files if path.name in DEPENDENCY_NAMES]
    project_files = [
        path
        for path in files
        if path.name == "project.pbxproj" or path.suffix in {".xcodeproj", ".xcworkspace"}
    ]

    report: dict[str, Any] = {
        "schema_version": 1,
        "project": str(project),
        "file_count": len(files),
        "xcode_project_files": [rel(path, project) for path in project_files],
        "dependency_files": [rel(path, project) for path in dependency_files],
        "info_plists": [info_plist_summary(path, project) for path in info_plists],
        "entitlements": [entitlement_summary(path, project) for path in entitlements],
        "privacy_manifests": [privacy_summary(path, project) for path in privacy],
        "storekit_configurations": [storekit_summary(path, project) for path in storekit],
        "risk_signals": scan_risk_signals(files, project, max_source_bytes),
        "app_bundle": inspect_app_bundle(app) if app else None,
    }
    report["observations"] = build_observations(report)
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Apple project evidence",
        "",
        f"- Project: `{report['project']}`",
        f"- Files scanned: {report['file_count']}",
        f"- Info.plist files: {len(report['info_plists'])}",
        f"- Entitlement files: {len(report['entitlements'])}",
        f"- Privacy manifests: {len(report['privacy_manifests'])}",
        f"- StoreKit configurations: {len(report['storekit_configurations'])}",
        "",
        "## Risk signals",
        "",
    ]
    if report["risk_signals"]:
        for name, paths in sorted(report["risk_signals"].items()):
            lines.append(f"- **{name}**: {', '.join(f'`{path}`' for path in paths)}")
    else:
        lines.append("- None detected by static pattern scanning.")
    lines.extend(["", "## Observations", ""])
    if report["observations"]:
        for item in report["observations"]:
            lines.append(f"- **{item['level']} / {item['topic']}**: {item['message']}")
    else:
        lines.append("- No deterministic observations. This is not a compliance verdict.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2
    app = Path(args.app).expanduser().resolve() if args.app else None
    report = collect_report(project, app, args.max_source_bytes)
    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
