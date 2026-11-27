# copier-kotlin-android

Rapid Android app foundation built with Kotlin, Jetpack Compose, Material 3, responsive phone/tablet layouts and an optional **separately installable Wear OS app**. It prioritizes getting working prototypes onto devices and packaging releases, with simple paths for AI coding agents.

```bash
uvx --from copier==9.19.1 copier copy gh:RuchirChawdhry/copier-kotlin-android my-app
cd my-app
task setup
task check
task test
task build
```

Requires JDK 17, Android command-line SDK, Task and Git. No Android Studio required. See the generated AGENTS.md and README for device tests and benchmarks. CI is shared via [ci-workflows](https://github.com/RuchirChawdhry/ci-workflows). The screenshot workflow replaces the current screenshot set. Release APKs are unsigned; configure signing before distribution.

## Choose your starting point

Copier asks only for features you want:

| Decision | Generated foundation |
| --- | --- |
| Device target | Phone/tablet Compose app; Wear OS companion (on by default) with its own watch UI, APK/AAB, manifest and shared `:core` logic |
| Layout | Single screen, adaptive navigation tabs, or phone drawer/tablet rail (default) |
| Native packs | Room database, CameraX, LAN discovery, Bluetooth, printing and Kotlin serialization, each with a starter Kotlin file |
| Optional platform packs | HTTP + Coil network, background WorkManager, Storage Access Framework, notifications, Robolectric |
| Visual components | Coil, Material 3 and Material 3 Adaptive by default; optional Compose Unstyled, JetCo, RikkaUI, Algolia, advanced bottom sheet, Sea Glass, FormInputs, Dateced and DejaVu |
| Source references | FlexiUI source recipes and [Composables UI](https://composables.com/ui) copy/paste components (not pretend Maven dependencies) |

For automation, the generated repo includes `task doctor`, `task dev`, `task device:inspect`, `task test:ui`, `task screenshots`, `task emulator:tablet:create`, `task release:phone` and (when selected) `task emulator:wear:create`, `task run:wear`, `task release:wear`. Its **Build release artifacts** action is manual-only and uploads APK/AAB artifacts; signing secrets are optional for local builds but mandatory before store submission. The screenshot action stays manual-only and is not triggered by CI or other workflows.

This is not a cross-platform UI compiler: one phone/tablet UI adapts to screen sizes, while the watch uses Wear Compose and an intentionally different small-screen experience. Business logic belongs in the small shared `:core` module when Wear is enabled; phone-specific native features still need platform and permission handling. Neither Play Store upload nor hardware validation happens automatically.

To verify generation across minimal, default and fully selected configurations without an SDK:

```bash
python3 tests/test_generation.py
```


## Documentation

- [Project website](https://ruchirchawdhry.github.io/copier-kotlin-android/) (after Pages deployment)
- [GitHub Wiki](https://github.com/RuchirChawdhry/copier-kotlin-android/wiki) (after wiki publication)
- [Documentation source](wiki/Home.md)

Both documentation destinations are generated from the same root wiki/ directory using shared CI workflows.
