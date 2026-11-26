plugins {
    id("com.android.application") version "8.9.2" apply false
    id("com.android.test") version "8.9.2" apply false
    id("org.jetbrains.kotlin.android") version "2.1.20" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.1.20" apply false
    id("androidx.baselineprofile") version "1.3.4" apply false
    id("org.jlleitschuh.gradle.ktlint") version "12.1.2"
    id("io.gitlab.arturbosch.detekt") version "1.23.8"
}

subprojects {
    apply(plugin = "org.jlleitschuh.gradle.ktlint")
}
detekt {
    buildUponDefaultConfig = true
    config.setFrom(files("config/detekt.yml"))
    source.setFrom(files("app/src/main/java", "app/src/test/java", "app/src/androidTest/java", "benchmark/src/main/java"))
}

