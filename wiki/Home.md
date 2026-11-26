# Build native Android apps for humans and agents.

A reusable Kotlin and Jetpack Compose foundation for command-line Android development.

```sh
uvx --from copier==9.19.1 copier copy gh:RuchirChawdhry/copier-kotlin-android my-app
```

## Highlights

- **Native Android**: Kotlin, Jetpack Compose and Material 3 with direct Android SDK access.
- **Agent-ready**: One task interface for setup, builds, tests and device operations.
- **Device verification**: Real emulator navigation tests and light/dark screenshots.
- **Measure performance**: Startup benchmarks, Baseline Profiles, memory and APK size reports.
- **Centralized CI**: Reuse shared workflows for consistent application validation.
- **Upgradeable foundation**: Track template answers for future Copier updates.

## Documentation

- [Getting started](Getting-Started): generate and build an application.
- [Architecture](Architecture): understand the application and benchmark modules.
- [Configuration](Configuration): template inputs and pinned Android toolchain.
- [Productivity toolkit](Productivity)
- [Development](Development): commands and agent workflow.
- [Testing and CI](Testing-and-CI): unit tests, lint and emulator checks.
- [Performance](Performance): measure startup, memory, frames and size.
- [Screenshots](Screenshots): capture and replace the documentation screenshots.
- [Release and distribution](Release-and-Distribution): release APKs and bundles.
- [Troubleshooting](Troubleshooting): diagnose common setup and device issues.
- [Wiki publishing](Wiki-Publishing): maintain these pages.

## Built with

Kotlin, Jetpack Compose, AndroidX, Gradle Kotlin DSL, JUnit, Robolectric, UI Automator, Macrobenchmark, ktlint, Detekt, ADB and Go Task.

---

Android · [MIT License](https://github.com/RuchirChawdhry/copier-kotlin-android/blob/main/LICENSE) · [GitHub](https://github.com/RuchirChawdhry/copier-kotlin-android) · [Central workflows](https://github.com/RuchirChawdhry/ci-workflows)
