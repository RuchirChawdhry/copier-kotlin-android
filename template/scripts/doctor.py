import json
import os
import shutil
import subprocess
import sys

checks = {name: shutil.which(name) for name in ("java", "sdkmanager", "adb", "emulator", "git", "python3")}
checks["ANDROID_HOME"] = os.environ.get("ANDROID_HOME")
checks["gradle_wrapper"] = os.path.isfile("gradlew")
checks["kvm_access"] = os.access("/dev/kvm", os.R_OK | os.W_OK)
if checks["java"]:
    checks["java17"] = 'version "17.' in subprocess.run(["java", "-version"], capture_output=True, text=True).stderr
required = ["java", "sdkmanager", "adb", "emulator", "git", "python3", "ANDROID_HOME", "gradle_wrapper", "java17"]
ok = all(checks.get(key) for key in required)
print(json.dumps({"ok": ok, "checks": checks}, indent=2))
sys.exit(0 if ok else 1)
