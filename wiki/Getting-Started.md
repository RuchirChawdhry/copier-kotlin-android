# Getting started

## Prerequisites

Use a Linux development machine (Ubuntu is the CI reference environment). Install JDK 17, Git, uv, Go Task and the Android SDK command-line tools. Set ANDROID_HOME and add the SDK's command-line tools, platform-tools and emulator directories to PATH. Accept the Android SDK licenses using sdkmanager --licenses.

Android Studio is optional. The template includes the Gradle Wrapper.

## Generate a project

```sh
uvx --from copier==9.19.1 copier copy gh:RuchirChawdhry/copier-kotlin-android my-app
cd my-app
task setup
task check
task test
task build
```

Answer the project name and application ID prompts. See [Configuration](Configuration).

The debug APK is generated under app/build/outputs/apk/debug/ after a successful build.

## Run on an Android device

Connect a device with USB debugging enabled or create an emulator:

```sh
sdkmanager 'system-images;android-35;google_apis;x86_64'
avdmanager create avd -n dev -k 'system-images;android-35;google_apis;x86_64'
export ANDROID_AVD_NAME=dev
task emulator
```

In a second terminal:

```sh
adb devices
task run
task test:ui
```

The emulator requires a compatible host architecture and virtualization support. Use the matching system image on other host architectures.

Continue with [Development](Development) and [Testing and CI](Testing-and-CI).
