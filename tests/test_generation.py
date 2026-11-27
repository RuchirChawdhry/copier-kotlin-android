"""Smoke-test Copier variants without requiring the Android SDK.

Run with: python3 tests/test_generation.py
"""

from __future__ import annotations

import json
import runpy
import shutil
import re
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
COPIER = ["uvx", "--from", "copier==9.19.1", "copier"]
NATIVE = ["room", "camera", "lan", "bluetooth", "printing", "serialization", "media"]
ADDONS = [
    "jetco",
    "rikkaui",
    "unstyled",
    "algolia",
    "advanced_sheet",
    "sea_glass",
    "form_inputs",
    "dateced",
    "dejavu",
    "flexiui",
]


def require(path: Path, present: bool = True) -> None:
    assert path.exists() == present, f"Expected present={present}: {path}"


def render(source: Path, destination: Path, data: dict[str, object]) -> None:
    answers = destination.parent / f"{destination.name}.yaml"
    # Strings, Booleans and lists suffice for this fixed test matrix.
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(repr(v) for v in value)}]")
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f"{key}: {value}")
    answers.write_text(("\n".join(lines) + "\n") if lines else "{}\n", encoding="utf-8")
    subprocess.run(
        [*COPIER, "copy", "--defaults", "--quiet", "--data-file", str(answers), str(source), str(destination)],
        check=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="android-copier-matrix-") as temporary:
        work = Path(temporary)
        # An untracked local change is otherwise ignored when Copier checks out a Git source.
        source = work / "source"
        source.mkdir()
        shutil.copy2(REPO / "copier.yml", source / "copier.yml")
        shutil.copytree(REPO / "template", source / "template")

        default = work / "default"
        render(source, default, {})
        subprocess.run(["python3", "scripts/test-tooling.py"], cwd=default, check=True)
        require(default / "wear/build.gradle.kts")
        require(default / "core/build.gradle.kts")
        require(default / "app/src/main/java/com/example/androidapp/AppViewModel.kt")
        require(default / "app/src/main/java/com/example/androidapp/NotesDatabase.kt", False)
        require(default / "docs/UI-LIBRARIES.md")
        design = default / "app/src/main/java/com/example/androidapp/AppDesign.kt"
        assert "GeneratedVisualStyle = VisualStyle.NATIVE" in design.read_text()
        require(default / ".github/workflows/release.yml")
        assert "workflow_dispatch:" in (default / ".github/workflows/release.yml").read_text()
        assert "push:" not in (default / ".github/workflows/screenshots.yml").read_text()
        for screenshot_action in [
            REPO / ".github/workflows/screenshots.yml",
            default / ".github/workflows/screenshots.yml",
        ]:
            assert "on:\n  workflow_dispatch:\n" in screenshot_action.read_text()
        for action in list((REPO / ".github/workflows").glob("*.yml")) + list(
            (default / ".github/workflows").glob("*.yml")
        ):
            if action.name != "screenshots.yml":
                assert "mode: screenshots" not in action.read_text(), action
        assert "dependencies {\n    implementation(project(\":core\"))" in (
            default / "app/build.gradle.kts"
        ).read_text()
        assert "import kotlinx.coroutines.launch\n\n@OptIn" in (
            default / "app/src/main/java/com/example/androidapp/AppNavigation.kt"
        ).read_text()
        scenarios = json.loads((default / "scripts/screenshot-scenarios.json").read_text())
        assert scenarios["layouts"]["phone"]["size"] == "540x1170"
        assert scenarios["layouts"]["rail"]["size"] == "800x1200"
        assert scenarios["layouts"]["wide"]["size"] == "1024x1280"
        assert scenarios["layouts"]["landscape"]["size"] == "960x540"
        for layout, spec in scenarios["layouts"].items():
            width, height = map(int, spec["size"].split("x"))
            dp_width = width * 160 / spec["density"]
            if layout == "phone":
                assert dp_width < 600
            if layout == "rail":
                assert 600 <= dp_width < 840
            if layout == "wide":
                assert dp_width >= 840
            if layout == "landscape":
                assert width > height and dp_width >= 600
        assert "screenshots:preview:" in (default / "Taskfile.yml").read_text()
        validator = runpy.run_path(str(default / "scripts/validate-screenshots.py"))
        assert len(validator["expected_names"](["phone"], ["light"])) == 8
        assert "light-phone-sheet-expanded.png" in validator["expected_names"](["phone"], ["light"])
        assert len(validator["expected_names"](list(scenarios["layouts"]), ["light", "dark"])) == 38

        def chunk(kind: bytes, payload: bytes) -> bytes:
            return (struct.pack(">I", len(payload)) + kind + payload +
                    struct.pack(">I", zlib.crc32(kind + payload)))

        sample = work / "sample.png"
        sample.write_bytes(
            bytes.fromhex("89504e470d0a1a0a")
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00\xff"))
            + chunk(b"IEND", b"")
        )
        validator["validate_png"](sample, (1, 1))
        try:
            validator["validate_png"](sample, (540, 1170))
        except ValueError as exc:
            assert "unexpected dimensions" in str(exc)
        else:
            raise AssertionError("Screenshot dimension validation accepted the wrong image size")

        lean = work / "lean"
        render(
            source,
            lean,
            {"include_wear": False, "ui_layout": "single", "visual_style": "editorial"},
        )
        assert "GeneratedVisualStyle = VisualStyle.EDITORIAL" in (
            lean / "app/src/main/java/com/example/androidapp/AppDesign.kt"
        ).read_text()
        require(lean / "wear", False)
        require(lean / "core", False)
        assert "include(\":wear\")" not in (lean / "settings.gradle.kts").read_text()
        assert "build:wear" not in (lean / "Taskfile.yml").read_text()
        assert "dependencies {\n    val composeBom" in (lean / "app/build.gradle.kts").read_text()

        full = work / "full"
        render(
            source,
            full,
            {
                "include_wear": True,
                "ui_layout": "tabs",
                "visual_style": "technical",
                "include_http": True,
                "capabilities": NATIVE,
                "ui_addons": ADDONS,
            },
        )
        app = full / "app/src/main/java/com/example/androidapp"
        assert "GeneratedVisualStyle = VisualStyle.TECHNICAL" in (
            app / "AppDesign.kt"
        ).read_text()
        for name in [
            "NotesDatabase.kt",
            "CameraPreview.kt",
            "LanDiscovery.kt",
            "BluetoothTools.kt",
            "PrintTools.kt",
            "JsonContracts.kt",
            "PermissionGate.kt",
            "MediaPlayerPreview.kt",
            "DateUtilities.kt",
        ]:
            require(app / name)
        manifest = (full / "app/src/main/AndroidManifest.xml").read_text()
        assert "android.permission.CAMERA" in manifest
        assert "android.permission.BLUETOOTH_SCAN" in manifest
        assert "android.permission.INTERNET" in manifest
        gradle = (full / "app/build.gradle.kts").read_text()
        assert "    alias(libs.plugins.ksp)\n    alias(libs.plugins.kotlin.serialization)\n}" in gradle
        assert "implementation(libs.compose.unstyled)" in gradle
        assert "implementation(libs.algolia.instantsearch)" in gradle
        assert "implementation(libs.dateced)" not in gradle
        assert "androidTestImplementation(libs.dejavu)" in gradle
        assert "NavigationSuiteScaffold" in (app / "AppNavigation.kt").read_text()
        assert "source recipe" in (full / "docs/UI-LIBRARIES.md").read_text()

        for destination in [default, lean, full]:
            app_sources = destination / "app/src/main/java/com/example/androidapp"
            theme = (app_sources / "AppTheme.kt").read_text()
            assert "typography = AppTypography" in theme
            assert "shapes = AppShapes" in theme
            assert "presetColorScheme(dark)" in theme
            assert "?: DefaultDynamicColors" in (
                app_sources / "SettingsStore.kt"
            ).read_text()
            assert "FlowRow(" in (app_sources / "SettingsScreen.kt").read_text()
            assert "ThemeMode.entries.chunked" not in (
                app_sources / "SettingsScreen.kt"
            ).read_text()
            assert "BottomSheetScaffold(" in (app_sources / "UiComponents.kt").read_text()
            assert "HomeBottomSheet(" in (app_sources / "App.kt").read_text()
            require(destination / "app/src/androidTest/java/com/example/androidapp/BottomSheetTest.kt")
            assert "| Visual style |" in (destination / "README.md").read_text()
            for path in destination.rglob("*"):
                assert not path.name.endswith(".jinja"), path
            for kotlin in destination.rglob("*.kt"):
                lines = kotlin.read_text().splitlines()
                imports = [line for line in lines if line.startswith("import ")]
                assert imports == sorted(imports), f"Unsorted imports: {kotlin}"
                assert all(len(line) <= 100 for line in lines), f"Long Kotlin line: {kotlin}"
            for workflow in (destination / ".github/workflows").glob("*.yml"):
                content = workflow.read_text()
                assert "{%" not in content and re.search(r"(?<!\$)\{\{", content) is None, workflow
        print("Copier generation matrix: default / lean / full passed")


if __name__ == "__main__":
    main()
