[app]
title = Sanemi Downloader Pro
package.name = sanemidownloaderpro
package.domain = org.sanemi
source.dir = .
source.exts = py,png,jpg,kv,atlas
version = 1.0

# متطلبات مشددة لتفادي أي نقص في الحزم داخل أندرويد
requirements = python3,kivy,yt-dlp,certifi,requests,urllib3,idna,charset-normalizer,setuptools

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
