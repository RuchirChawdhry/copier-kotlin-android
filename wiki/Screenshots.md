# Screenshots

Capture actual Android emulator screens with the native Android instrumentation screenshot API.

## Local capture

Start one Android emulator, then run:

```sh
task screenshots
```

The script temporarily changes the emulator's display metrics to exercise real responsive layouts. It restores the original metrics, rotation settings and night mode on exit. Both debug and instrumentation APKs remain installed. A physical device is intentionally not supported by this resizing script.

## Screenshot gallery

Each layout is captured in light and dark mode:

| Layout | Screens |
| --- | --- |
| Phone | Home, **expanded bottom sheet**, drawer, Settings, toggled settings, About, search results, empty search |
| Medium tablet | Persistent navigation rail, **expanded bottom sheet**, Settings |
| Expanded tablet | Expanded sidebar, **expanded bottom sheet**, collapsed sidebar, Settings |
| Landscape phone | Expanded sidebar, **expanded bottom sheet**, collapsed sidebar, Settings |

The 38 PNGs are stored directly under the root screenshots/ directory. Filenames use the theme, layout and screen, for example dark-phone-sheet-expanded.png and light-wide-sheet-expanded.png. Expanded-sheet captures verify that the swipe-up gesture reveals the shortcut buttons, not just the collapsed handle.

Browse [repository screenshots](https://github.com/RuchirChawdhry/copier-kotlin-android/tree/main/screenshots).

## GitHub Actions

Open [Android UI screenshots](https://github.com/RuchirChawdhry/copier-kotlin-android/actions/workflows/screenshots.yml) and select Run workflow on the default branch.

The capture job generates a fresh app, builds the debug and test APKs, starts a hardware-accelerated Android emulator and exercises all four viewport configurations in both themes. Instrumentation asserts the active layout, selected destinations and preservation of the counter state. Each PNG is validated before publication. Failed captures preserve the previous gallery and retain diagnostic artifacts.

The publication job replaces the complete screenshot directory. The screenshot manifest lives in scripts/validate-screenshots.py. Update it and the instrumentation test when adding screens.

See [Testing and CI](Testing-and-CI).
