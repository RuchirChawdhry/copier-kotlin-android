# Testing and CI

## Validation layers

| Layer | Tools | Environment |
| --- | --- | --- |
| Template generation | Copier | Ubuntu |
| Formatting | ktlint | JVM |
| Static analysis | Detekt and Android Lint | JVM |
| Unit tests | JUnit and Robolectric | JVM |
| UI interaction | Compose UI Test and UI Automator | Android device |
| Release build | Gradle and R8 | JVM |

The sample tests cover counter behavior, application label configuration, navigation and state retention.

## Shared workflows

The template and generated applications call [kotlin-android.yml](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/kotlin-android.yml).

- Android CI: push, pull request and manual validation. Template runs also generate an alternate application ID and check invalid input rejection.
- Android compatibility: manual API 26 and 35 device matrix.
- Android screenshots: manual capture and publication only; not a dependency of CI.

The runner uses Ubuntu 24.04, JDK 17 and an x86-64 Android emulator with KVM acceleration. Artifacts are configured to include APKs, test reports, screenshots and device logs where produced.

## Screenshot feedback loop

Generated projects provide two useful speeds:

1. `task screenshots:preview` captures the light-theme phone scenarios into `reports/screenshot-preview/` for a quick visual review during development. It never changes committed screenshots.
2. `task screenshots` captures every declared layout in light and dark mode. **Actions → Android UI screenshots → Run workflow** runs the same full capture on a disposable emulator and commits the validated images to `screenshots/` on the default branch.

The manifest (`scripts/screenshot-scenarios.json`) specifies deterministic layouts and test names. Pixel output is intentionally small enough to review quickly: phone 540×1170, medium tablet 800×1200, expanded tablet 1024×1280, and landscape 960×540. Density overrides still test narrow, medium and expanded Compose layouts. The validator rejects missing or extra files, corrupt PNG chunks and wrong dimensions. Failure artifacts include instrumentation output and device logs.

For future pixel-diff regression testing, consider [Roborazzi](https://github.com/takahirom/roborazzi) or [Paparazzi](https://github.com/cashapp/paparazzi) against isolated `@Preview` compositions. Those JVM tools complement real emulator behavior and capture; they do not replace it.

## Status and limits

Consult [Actions](https://github.com/RuchirChawdhry/copier-kotlin-android/actions) for current validation results. Emulator captures test responsive navigation layouts but do not establish physical-device behavior for BLE, cameras, LAN or other hardware. The Copier update lifecycle is not yet a tested CI stage.

See [Troubleshooting](Troubleshooting) for failure diagnosis.
