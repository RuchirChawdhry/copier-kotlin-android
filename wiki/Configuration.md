# Configuration

## Copier inputs

| Input | Default | Purpose |
| --- | --- | --- |
| project_name | Android App | Gradle project name and Android display label |
| application_id | com.example.androidapp | Android application ID, namespace and source packages |

The project name validator restricts input to ASCII letters, digits, spaces, underscores and hyphens, starting with a letter. The application ID validator requires lowercase reverse-domain segments. Choose a unique ID for distributable apps. Avoid Kotlin reserved keywords in package segments.

The template stores its answers for future Copier updates. The full update lifecycle has not yet been certified; inspect generated diffs before applying an update.

## Toolchain

| Component | Pinned baseline |
| --- | --- |
| JDK | 17 |
| Gradle | 8.11.1 |
| Android Gradle Plugin | 8.9.2 |
| Kotlin | 2.1.20 |
| Compose BOM | 2025.04.01 |
| compileSdk / targetSdk | 35 |
| minSdk | 26 |

These are the configured versions, not a claim that they are the latest or that the target meets current Google Play submission policy. The benchmark module requires API 28 or above.

Dependency and plugin versions live in gradle/libs.versions.toml. SDK values live in gradle.properties. Optional capabilities are described in [Productivity toolkit](Productivity).

Do not commit local.properties, keystores or signing credentials. See [Release and distribution](Release-and-Distribution).
