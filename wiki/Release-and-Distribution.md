# Release and distribution

## Build artifacts

```sh
task build
task release
```

The debug command builds an installable debug APK. The release command invokes Gradle assembleRelease and bundleRelease. Check app/build/outputs/apk/release/ and app/build/outputs/bundle/release/ after a successful build.

## Signing

Release artifacts are unsigned by default. Configure an application-specific release signing configuration before distribution. Protect the keystore and passwords outside source control. For CI signing, use appropriately restricted Actions secrets.

## Publishing

Check Google Play's current target API and distribution requirements before publishing. Do not assume that the pinned target SDK satisfies current store policy.

Automatic APK/AAB release publication and tag-triggered release workflows are not implemented yet. Dependabot configuration is included in generated projects for Gradle and Actions dependencies.

See [Configuration](Configuration) for the pinned toolchain and [Performance](Performance) for release optimization.
