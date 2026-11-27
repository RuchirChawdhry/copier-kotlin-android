# Architecture

The template produces a native Android application, not a web application embedded in a WebView.

## Project layout

| Path | Responsibility |
| --- | --- |
| app/src/main/ | Activity, Compose UI, Android resources and manifest |
| wear/ (optional) | Separate Wear OS Compose Material 3 application, round-screen entrypoint and independent release artifact |
| core/ (optional) | Lightweight Kotlin business logic shared by phone and watch |
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

MainActivity enables edge-to-edge rendering and sets the Compose content. App defines a Material 3 color scheme following the system theme, a responsive navigation shell and three sample destinations: Home, Settings and About. `AppViewModel` stores navigation and counter state across configuration changes; DataStore keeps settings. Coil supplies image loading.

The navigation shell selects a bottom bar plus modal drawer below 600 dp, a persistent rail from 600 dp, and an expanded permanent drawer from 840 dp (or a landscape window at least 600 dp wide). The expanded drawer can collapse to a rail and reopen. All destinations share the same saveable state. Navigation components use Material 3, grouped drawer sections and a replaceable vector logo.

Copier lets you select a single-screen shell, Material 3 adaptive navigation tabs or the original responsive drawer/rail. The sample demonstrates navigation and state preservation. Replace it with application-specific functionality rather than treating the counter as a required subsystem.

The watch is a separate app using Wear Compose Material 3, not a shrunk version of the phone UI. It shares a small logic module with the handheld target, ready for feature-specific domain models. Phone/tablet layouts share one APK; watch packaging and store/device behavior are different. Neither the `:core` module nor this template automatically synchronizes data over Bluetooth or the network.

Use the Android SDK and AndroidX for platform capabilities. Select Room, CameraX, LAN, Bluetooth, printing and/or serialization in Copier to get manifest entries, dependencies and starter APIs only for those capabilities. Add native C, C++ or Rust libraries only where measurements justify a native computation layer. No NDK integration is included by default.

See [Performance](Performance) and [Testing and CI](Testing-and-CI).
