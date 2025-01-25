[app]

# title of the application
title = Kivy Remote Shell

# package name
package.name = remoteshell

# package domain (mostly used for android/ios package)
package.domain = org.kivy

# indicate where the source code is living
source.dir = .
source.include_exts = py,png,kv,rst

# search the version information into the source code
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# requirements of the app
requirements = android,cryptography,pyasn1,bcrypt,attrs,twisted,kivy,docutils,pygments,cffi

# android specific
android.permissions = INTERNET, WAKE_LOCK, CAMERA, VIBRATE, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION, SEND_SMS, CALL_PRIVILEGED, CALL_PHONE, BLUETOOTH

#android.sdk=21

#android.api=22
android.accept_sdk_license=True
android.wakelock=True
orientation=portrait
fullscreen=True
p4a.branch = release-2022.12.20

#presplash.filename= 

[buildozer]
log_level = 2
warn_on_root = 1
