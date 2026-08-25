[app]
title = Challenge Timer
package.name = challengetimer
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
icon.filename = %(source.dir)s/icon.png
version = 0.1
requirements = python3,kivy
orientation = sensor
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
