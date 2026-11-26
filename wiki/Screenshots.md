# Screenshots

The template uses real Android emulator screenshots, captured from the instrumented navigation test using UI Automator.

## Local capture

Boot one emulator or connect one device, then run:

```sh
task screenshots
```

The script switches between light and dark system themes, runs UI tests, pulls the captures and checks that both screens exist before replacing the output directory. It attempts to restore the previous night mode on exit.

Expected output:

```text
screenshots/
├── light/
│   ├── home.png
│   └── settings.png
└── dark/
    ├── home.png
    └── settings.png
```

## GitHub Actions

Open Actions, select Android screenshots and choose Run workflow on the default branch. The workflow is configured to upload the captures and replace the existing screenshots directory in the repository.

Browse [repository screenshots](https://github.com/RuchirChawdhry/copier-kotlin-android/tree/main/screenshots) after the first successful capture. The directory may not exist before that run.

When adding a screen, add an instrumented navigation step and a stable screenshot filename. Do not commit mockups as evidence of actual emulator execution.

Screenshot regression comparisons are not included yet. See [Testing and CI](Testing-and-CI).
