# Configuration

## Copier inputs

| Input | Default | Purpose |
| --- | --- | --- |
| project_name | Android App | Gradle project name and Android display label |
| application_id | com.example.androidapp | Android application ID, namespace and source packages |
| ui_layout | adaptive | Single screen, navigation suite tabs or responsive drawer/rail |
| include_wear | true | Generate watch APK/AAB and lightweight shared core |
| wear_standalone | true | Watch standalone metadata (shown only when Wear is enabled) |
| capabilities | none | Multiselect: Room, CameraX, LAN, Bluetooth, printing, serialization |
| ui_addons | none | Multiselect: selected UI, form, search and diagnostics packages |
| include_http | false | OkHttp, Coil network image fetching, Internet permission |
| include_background_jobs | false | WorkManager and a sample job |
| include_file_access | false | Storage Access Framework picker |
| include_notifications | false | Notification sample |
| include_robolectric | false | Robolectric JVM tests |

The project name validator restricts input to ASCII letters, digits, spaces, underscores and hyphens, starting with a letter. The application ID validator requires lowercase reverse-domain segments. Choose a unique ID for distributable apps. Avoid Kotlin reserved keywords in package segments.

The template stores its answers for future Copier updates. Choices are native [Copier multiselect/conditional questions](https://copier.readthedocs.io/), with optional files and modules rendered only when selected. `copier update` is available for generated Git repositories, but inspect its three-way merge and keep changes committed before updating; migration of heavily edited projects is not guaranteed.

## Toolchain

| Component | Pinned baseline |
| --- | --- |
| JDK | 17 |
| Gradle | 9.6.0 |
| Android Gradle Plugin | 9.5.1 |
| Kotlin | 2.4.21 |
| Compose BOM | 2026.08.00 |
| compileSdk / targetSdk | 37 / 36 |
| minSdk | 26 |

These are the configured versions, not a promise of current Google Play submission eligibility. The benchmark module requires API 28 or above. AGP 9 uses built-in Kotlin; do not reapply the obsolete `org.jetbrains.kotlin.android` plugin.

Dependency and plugin versions live in `gradle/libs.versions.toml`. SDK values live in `gradle.properties`. `android.platformPackage=37.0` is the SDK Manager package suffix for API 37; the Gradle compile SDK is still 37. Opt-in UI libraries are described in the generated `docs/UI-LIBRARIES.md` and [Productivity toolkit](Productivity).

Do not commit local.properties, keystores or signing credentials. See [Release and distribution](Release-and-Distribution).
