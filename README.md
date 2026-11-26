# copier-kotlin-android

Native Android starter: Kotlin, Jetpack Compose, Material 3, Gradle, unit and device tests, automated screenshots and performance instrumentation.

```bash
uvx --from copier==9.19.1 copier copy gh:RuchirChawdhry/copier-kotlin-android my-app
cd my-app
task setup
task check
task test
task build
```

Requires JDK 17, Android command-line SDK, Task and Git. No Android Studio required. See the generated AGENTS.md and README for device tests and benchmarks. CI is shared via [ci-workflows](https://github.com/RuchirChawdhry/ci-workflows). The screenshot workflow replaces the current screenshot set. Release APKs are unsigned; configure signing before distribution.


## Documentation

- [Project website](https://ruchirchawdhry.github.io/copier-kotlin-android/) (after Pages deployment)
- [GitHub Wiki](https://github.com/RuchirChawdhry/copier-kotlin-android/wiki) (after wiki publication)
- [Documentation source](wiki/Home.md)

Both documentation destinations are generated from the same root wiki/ directory using shared CI workflows.
