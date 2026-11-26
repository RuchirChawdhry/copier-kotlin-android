# Agent instructions

- Use Kotlin and Compose; reuse Android SDK and AndroidX APIs.
- Run task check, task test, task build before committing. Run task test:ui after UI changes.
- Use adb to install, launch, inspect logcat, and dump UI hierarchy. Prefer Compose test tags for UI tests.
- Keep the sample counter and settings screens replaceable. Add tests and screenshot capture for new screens.
- Keep dependencies minimal. Do not add native code without measuring a bottleneck.
- Use release builds and physical devices for performance claims. Keep generated baseline profiles in version control.
- Do not commit local.properties, signing keys or secrets.

