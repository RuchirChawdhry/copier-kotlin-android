# Architecture

The template produces a native Android application, not a web application embedded in a WebView.

## Project layout

| Path | Responsibility |
| --- | --- |
| app/src/main/ | Activity, Compose UI, Android resources and manifest |
| app/src/test/ | JVM unit tests and Robolectric tests |
| app/src/androidTest/ | Instrumented navigation and screenshot tests |
| benchmark/ | Startup Macrobenchmark and Baseline Profile generator |
| config/detekt.yml | Static analysis configuration |
| gradle/wrapper/ | Pinned Gradle distribution and wrapper |
| scripts/ | Device, screenshot and measurement commands |
| Taskfile.yml | Unified developer commands |
| AGENTS.md | Agent development instructions |
| .github/workflows/ | Calls to shared CI workflows |

## Runtime

MainActivity enables edge-to-edge rendering and sets the Compose content. App defines a Material 3 color scheme following the system theme, a scaffold and two sample destinations: Home and Settings. The sample counter uses saveable state.

The sample demonstrates navigation and state preservation. Replace it with application-specific functionality rather than treating the counter as a required subsystem.

Use the Android SDK and AndroidX for platform capabilities. Add native C, C++ or Rust libraries only where measurements justify a native computation layer. No NDK integration is included by default.

See [Performance](Performance) and [Testing and CI](Testing-and-CI).
