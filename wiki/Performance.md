# Performance

Measure before optimizing. Kotlin and Compose provide a native foundation, but performance depends on implementation, device and workload.

| Command | Output or action |
| --- | --- |
| task benchmark | Run the Macrobenchmark device suite |
| task benchmark:startup | Measure cold startup |
| task benchmark:profile | Generate a Baseline Profile |
| task benchmark:memory | Capture adb dumpsys meminfo |
| task benchmark:scroll | Capture adb dumpsys gfxinfo frame statistics |
| task benchmark:size | Build release APK and record file size |
| task benchmark:report | List report and benchmark output paths |

## Measurement procedure

Use a physical device running API 28 or later for Macrobenchmark. Use a release-like build, stable device conditions and repeated measurements. The supplied startup benchmark requests five cold-start iterations; examine the results and Perfetto traces where generated.

For memory and frame measurements, launch the app and reproduce the same interaction before collecting the reports. The frame command is a snapshot of rendering statistics, not an automated scrolling workload.

The release configuration enables R8 and resource shrinking. Generate Baseline Profiles for representative critical journeys and retain the generated profile files in version control.

## Limitations

Performance commands are scaffolded but have not been certified by device execution. No numerical startup or RAM claim is made. There is no Microbenchmark module or automated performance threshold gate yet. Use emulator tests for functional validation, not hardware performance comparisons.
