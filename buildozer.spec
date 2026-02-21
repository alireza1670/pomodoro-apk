[app]
title = Pomodoro
package.name = pomodoro
package.domain = org.alireza
source.dir = .
source.include_exts = py
version = 0.1

requirements = python3,kivy
orientation = portrait

fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
