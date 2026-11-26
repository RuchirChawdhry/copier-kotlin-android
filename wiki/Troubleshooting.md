# Troubleshooting

| Symptom | Action |
| --- | --- |
| sdkmanager not found | Install the Android SDK command-line tools and update PATH. |
| SDK license error | Run sdkmanager --licenses and accept the required licenses. |
| Gradle Java mismatch | Select JDK 17 and check java -version and ./gradlew --version. |
| Missing Android platform | Run task setup to install platform 35 and build tools. |
| Emulator fails to boot | Check host virtualization, KVM permissions and the system image architecture. |
| ADB reports multiple devices | Disconnect extras or select the intended device with ANDROID_SERIAL. |
| Formatting failure | Run task fix and inspect the changes. |
| Unit test failure | Inspect app/build/test-results and rerun task test. |
| Instrumented failure | Inspect device state, screenshots, Logcat and Android test reports. |
| Screenshot publication fails | Inspect the capture and publish jobs; verify repository write permissions. |
| Pages or wiki publication fails | See [Wiki publishing](Wiki-Publishing). |

## Diagnose a failing CI run

Open [Actions](https://github.com/RuchirChawdhry/copier-kotlin-android/actions), select the failing run and inspect the first failed step. Download the reports and logs if the workflow uploaded them. Reproduce the matching command locally instead of suppressing a check.

For Gradle detail, append --stacktrace to the failing Gradle command. Do not treat a generated project as validated until its checks and build pass.
