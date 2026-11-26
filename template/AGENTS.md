# Android development guide

## Start here
- Ubuntu: run bash scripts/bootstrap.sh once (or task bootstrap if Task is installed). Review SDK licenses.
- Run task doctor before debugging environment failures; task doctor:json emits the same JSON.
- Run task dev to boot a headless AVD, install and launch the app. Set ANDROID_SERIAL for multiple devices.

## Architecture
- Keep one application module unless separation solves a real problem.
- App.kt owns app state; Screen.kt registers destinations. AppNavigation.kt and NavigationComponents.kt implement the adaptive shell.
- SettingsStore.kt persists preferences using DataStore; SettingsScreen.kt edits them; AppTheme.kt defines themes.
- Reuse UiComponents.kt or native Material 3 components; avoid unnecessary abstractions.
- OptionalIntegrations.kt contains selected platform examples. Do not add unused permissions or dependencies.
- Add string resources for new production UI and accessible descriptions for nondecorative icons.

## Feedback loop
- task fix formats; task check runs static checks; task test runs JVM tests; task build compiles the APK.
- Run task test:tooling for host scripts and task test:ui after navigation or UI changes. CI uses the same rules and collects reports.
- task device:inspect returns the UI hierarchy as JSON. Use stable Compose test tags; task device:tap -- TAG taps a uniquely matching node.
- task device:restart, task device:screenshot, task device:crashes and task device:info diagnose a running app.
- Clear app data only when explicitly intended; task device:clear -- --confirm is destructive.
- task screenshots exercises the real emulator. Update the scenario JSON and instrumentation test together.

## Dependencies and performance
- gradle/libs.versions.toml is the version catalog; gradle.properties owns SDK configuration.
- Prefer Android SDK and AndroidX. Enable extra capabilities only as needed.
- task benchmark:size, task benchmark:memory, task benchmark:scroll and task benchmark collect measurements; task benchmark:report creates JSON and HTML.
- Runtime comparisons require physical devices and equivalent workloads. Frame statistics are not an automated scroll benchmark.
- Never disable lint to hide failures. Do not commit local.properties, keystores or secrets.
