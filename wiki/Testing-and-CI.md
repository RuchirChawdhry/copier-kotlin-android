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
- Android screenshots: manual capture and publication.

The runner uses Ubuntu 24.04, JDK 17 and an x86-64 Android emulator with KVM acceleration. Artifacts are configured to include APKs, test reports, screenshots and device logs where produced.

## Status and limits

The initial runs failed during SDK setup because the Android setup action requested the obsolete tools package. The shared workflow now explicitly requests platform-tools and installs the required SDK components. A passing end-to-end run is not established. Consult [Actions](https://github.com/RuchirChawdhry/copier-kotlin-android/actions) for actual outcomes. The extended matrix does not yet establish ARM64, tablet, accessibility or landscape compatibility. The Copier update lifecycle is not yet a tested CI stage.

See [Troubleshooting](Troubleshooting) for failure diagnosis.
