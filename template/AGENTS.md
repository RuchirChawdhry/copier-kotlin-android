# Agent guide: rapid Android delivery

Aim to get a working user-visible prototype on a device in the first iteration. This is a small app foundation, not an enterprise architecture kit.

## First steps

- `task doctor` checks prerequisites; `task dev` boots a phone emulator and installs the app. Run `task test:tooling` for host tooling.
- Read `README.md` to see which Copier capability packs, UI libraries and targets were selected.
- Read `gradle/libs.versions.toml` before adding dependencies. Use the SDK, AndroidX and existing modules when possible.

## Where code goes

- `app` is the phone/tablet UI and Android entrypoint; `AppViewModel.kt` owns screen and sample counter state. `SettingsStore.kt` is the DataStore example.
- `AppNavigation.kt` is the responsive shell (single, tabs or adaptive); `UiComponents.kt` is the place for reusable components.
- `core`, if present, holds logic shared with the separate `wear` app. Keep this lightweight. A watch needs its own round-screen Compose UI and manifest.
- Optional capability starter files (Room, CameraX, LAN discovery, Bluetooth, printing, serialization) compile only when selected. Ask for runtime permissions and handle unavailable hardware before invoking features.
- Prefer feature-oriented files for each new screen. Extract modules only when sharing or build speed warrants it. Never store credentials in source or the APK.

## Agent feedback loop

- `task fix` formats. `task check` runs ktlint, detekt and Android lint. `task test` executes unit tests; `task test:ui` runs instrumented tests.
- `task device:list`, `task device:info`, `task device:inspect` (structured UI hierarchy), `task device:tap -- TAG`, `task device:screenshot` and `task device:crashes` support autonomous debugging. Use stable Compose test tags and accessible labels.
- `task screenshots` is manual. It updates generated image outputs only when requested; do not tie screenshot jobs into other workflows.
- Check compact phone, expanded tablet and, if generated, round Wear OS emulator configurations before release. Simulators do not replace hardware validation of camera, BLE, LAN or wearable interactions.

## Build and publish

- `task build:phone`, `task release:phone` build the handheld variant; when available `task build:wear`, `task release:wear` build the companion. `task release` packages all selected artifacts.
- The manual release GitHub Action uploads artifacts; it does **not** publish to Google Play. Store submission, signing and version increments remain explicit user actions.
- Run `task benchmark` only on a suitable device to collect meaningful traces. Do not confuse sample frame stats with reproducible benchmarks.
- Never commit `local.properties`, SDK credentials, Play signing keys, keystores or secrets.
