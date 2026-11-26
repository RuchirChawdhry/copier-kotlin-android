# Screenshots

Capture real Android application screens on an emulator using UI Automator. Each capture verifies the system theme before saving the image.

## Local capture

Start one emulator or connect one device, then run:

```sh
task screenshots
```

The script runs the navigation test in each theme and transfers PNG files from the debug app's private storage using ADB. The complete capture set is validated before replacing the previous directory. It attempts to restore the original system theme on exit.

## Screenshot gallery

All published PNG files live directly in the repository's root screenshots directory:

```text
screenshots/
├── dark-home.png
├── dark-settings.png
├── light-home.png
└── light-settings.png
```

Browse [repository screenshots](https://github.com/RuchirChawdhry/copier-kotlin-android/tree/main/screenshots).

## GitHub Actions

Open [Android UI screenshots](https://github.com/RuchirChawdhry/copier-kotlin-android/actions/workflows/screenshots.yml) and select Run workflow on the default branch.

The capture job generates a fresh app, builds the debug and test APKs, starts a hardware-accelerated Android emulator, and captures both themes. The publication job verifies the entire dedicated PNG artifact, replaces the root screenshots directory and commits only changed files. Failed captures preserve the existing gallery. The template repository also runs capture when its screenshot workflow file changes.

When adding a screen, add a navigation assertion, a stable filename and update the capture and publication manifests. Ordinary UI tests do not write screenshots unless capture mode is explicitly requested.

See [Testing and CI](Testing-and-CI).
