# Release and distribution

## Build artifacts

```sh
task build
task release
task release:phone
# task release:wear (when Wear was selected)
```

The debug command builds installable debug APKs. The release command invokes Gradle assembleRelease and bundleRelease for generated targets. Check `app/build/outputs/apk/release/` and `app/build/outputs/bundle/release/`, and (when enabled) `wear/build/outputs/`. The watch has a separate APK/AAB, but shares the Android application ID and signing key with the companion phone app; it uses an offset version code to keep the artifacts distinct.

## Signing

Release artifacts are unsigned by default. Set `ANDROID_SIGNING_STORE_FILE`, `ANDROID_SIGNING_STORE_PASSWORD`, `ANDROID_SIGNING_KEY_ALIAS` and `ANDROID_SIGNING_KEY_PASSWORD` to use a private signing key locally. Protect the keystore and passwords outside source control.

For the manual GitHub Actions release run, define `ANDROID_KEYSTORE_BASE64` (base64 of the keystore) plus the three password/alias secrets. The workflow writes the keystore to the runner's temporary directory, builds both target packages and uploads output artifacts. Without those secrets, the run packages unsigned release outputs for local evaluation, not store-ready bundles.

## Publishing

Check Google Play's current target API and distribution requirements before publishing. Do not assume that the pinned target SDK satisfies current store policy.

For a companion phone and Wear OS app under the same Play listing, follow the [Wear OS packaging guide](https://developer.android.com/training/wearables/packaging): Google recommends a common package name and signing key, separate version codes, and **Multi-APK delivery** for the paired artifacts. Two locally generated AABs are not automatically one combined Play release. Review phone and watch delivery on the Play Console separately.

Choose **Actions → Build release artifacts → Run workflow**. This workflow is `workflow_dispatch` only: it is never automatically triggered by CI, tags or pushes. Uploading to Google Play and checking the listing, screenshots, compatibility and version codes are manual user actions. Dependabot configuration is included in generated projects for Gradle and Actions dependencies.

See [Configuration](Configuration) for the pinned toolchain and [Performance](Performance) for release optimization.
