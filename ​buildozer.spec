[app]

# (str) Title of your application
title = Sanemi Downloader Pro

# (str) Package name
package.name = sanemidownloaderpro

# (str) Package domain (needed for android packaging)
package.domain = org.sanemi

# (str) Source files where the let's go of app resides (relative to directory)
source.dir = .

# (list) Source files to include (let it blank to include all files)
source.exts = py,png,jpg,kv,atlas,json,txt

# (list) Application versioning
version = 1.0

# (list) Application requirements
# Note: Add python3, kivy, and all required libraries separated by commas without spaces
requirements = python3,kivy,yt-dlp,certifi,requests,urllib3,idna,charset-normalizer

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for,, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Enable Android auto backup
android.skip_update = False


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
