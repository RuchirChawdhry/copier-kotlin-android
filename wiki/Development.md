# Development

Run commands from the generated project root.

| Command | Purpose |
| --- | --- |
| task setup | Install SDK components and the ktlint Git hook |
| task fix | Format Kotlin code |
| task check | Run formatting, Detekt and Android Lint checks |
| task test | Run JVM tests |
| task build | Build the debug APK |
| task release | Build release APK and AAB |
| task emulator | Start the AVD named by ANDROID_AVD_NAME |
| task install | Install the debug APK |
| task run | Install and launch the application |
| task test:ui | Run instrumented UI tests |
| task screenshots | Capture both system themes |
| task logs | Retrieve Logcat output |
| task test:all | Run checks, tests, build and UI tests |

## Agent workflow

1. Read AGENTS.md and the relevant application sources.
2. Implement a focused change using established Android APIs.
3. Run task fix, task check, task test and task build.
4. For UI changes, launch an emulator and run task test:ui.
5. Inspect failures and capture evidence before reporting completion.

Prefer Compose test tags for UI targeting. For device-level inspection:

```sh
adb shell uiautomator dump /sdcard/window.xml
adb shell cat /sdcard/window.xml
adb logcat -d
```

The accessibility hierarchy may omit custom-rendered content. Use screenshots when the hierarchy is insufficient. See [Screenshots](Screenshots).
