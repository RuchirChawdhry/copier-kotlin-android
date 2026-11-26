# Productivity toolkit

The generated application includes a command-line development environment, native UI components and opt-in integrations.

## Bootstrap and device operations

Install Git and uv, generate the project, then run bash scripts/bootstrap.sh (or task bootstrap if Task is installed) and accept SDK licenses. Missing Go Task is installed from a pinned, checksum-verified release. The script installs missing Ubuntu prerequisites, provisions command-line tools and creates the default AVD. Use task doctor to inspect toolchain readiness and task dev to launch the app.

Use task device:list, task device:inspect, task device:tap -- TAG, task device:screenshot and task device:crashes to interact with the selected device. Set ANDROID_SERIAL explicitly when several devices are connected. The device CLI emits JSON, including errors for ADB failures.

## Settings and components

DataStore persists the theme and dynamic color preference. The settings screen provides system, light, dark, AMOLED and Solarized modes and a reset action. UiComponents.kt includes a search field, empty/error/loading states and a confirmation dialog. These are small examples intended to be adapted to actual application requirements.

## Optional capabilities

Copier prompts for Robolectric, OkHttp, WorkManager, document selection and notifications. Defaults are off. The HTTP and notification options add their respective manifest permissions. Optional integrations are starting points, not complete product features.

## Reports

Run task benchmark:size, task benchmark:memory and task benchmark:scroll to collect available measurements, then task benchmark:report. Reports are saved under reports/performance, including current.json, comparison.json and index.html. Copy a comparable current.json to baseline.json to compare a later run. Macrobenchmark results and Perfetto traces are included when available.

See [Development](Development), [Performance](Performance) and [Screenshots](Screenshots).
