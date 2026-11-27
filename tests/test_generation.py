"""Smoke-test Copier variants without requiring the Android SDK.

Run with: python3 tests/test_generation.py
"""

from __future__ import annotations

import shutil
import re
import subprocess
import tempfile
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
        require(default / "wear/build.gradle.kts")
        require(default / "core/build.gradle.kts")
        require(default / "app/src/main/java/com/example/androidapp/AppViewModel.kt")
        require(default / "app/src/main/java/com/example/androidapp/NotesDatabase.kt", False)
        require(default / "docs/UI-LIBRARIES.md")
        require(default / ".github/workflows/release.yml")
        assert "workflow_dispatch:" in (default / ".github/workflows/release.yml").read_text()
        assert "push:" not in (default / ".github/workflows/screenshots.yml").read_text()
        assert "dependencies {\n    implementation(project(\":core\"))" in (
            default / "app/build.gradle.kts"
        ).read_text()
        assert "import kotlinx.coroutines.launch\n\n@OptIn" in (
            default / "app/src/main/java/com/example/androidapp/AppNavigation.kt"
        ).read_text()

        lean = work / "lean"
        render(source, lean, {"include_wear": False, "ui_layout": "single"})
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
                "include_http": True,
                "capabilities": NATIVE,
                "ui_addons": ADDONS,
            },
        )
        app = full / "app/src/main/java/com/example/androidapp"
        for name in [
            "NotesDatabase.kt",
            "CameraPreview.kt",
            "LanDiscovery.kt",
            "BluetoothTools.kt",
            "PrintTools.kt",
            "JsonContracts.kt",
            "PermissionGate.kt",
            "MediaPlayerPreview.kt",
        ]:
            require(app / name)
        manifest = (full / "app/src/main/AndroidManifest.xml").read_text()
        assert "android.permission.CAMERA" in manifest
        assert "android.permission.BLUETOOTH_SCAN" in manifest
        assert "android.permission.INTERNET" in manifest
        gradle = (full / "app/build.gradle.kts").read_text()
        assert "implementation(libs.compose.unstyled)" in gradle
        assert "implementation(libs.algolia.instantsearch)" in gradle
        assert "androidTestImplementation(libs.dejavu)" in gradle
        assert "NavigationSuiteScaffold" in (app / "AppNavigation.kt").read_text()
        assert "source recipe" in (full / "docs/UI-LIBRARIES.md").read_text()

        for destination in [default, lean, full]:
            for path in destination.rglob("*"):
                assert not path.name.endswith(".jinja"), path
            for workflow in (destination / ".github/workflows").glob("*.yml"):
                content = workflow.read_text()
                assert "{%" not in content and re.search(r"(?<!\$)\{\{", content) is None, workflow
        print("Copier generation matrix: default / lean / full passed")


if __name__ == "__main__":
    main()
