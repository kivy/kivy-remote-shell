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
requirements = hostpython2,android,cryptography,pyasn1,pyjnius,pycrypto,twisted,kivy,docutils,pygments,cffi

# android specific
android.permissions = INTERNET, WAKE_LOCK, CAMERA, VIBRATE, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION, SEND_SMS, CALL_PRIVILEGED, CALL_PHONE

#android.sdk=21

#android.api=22

android.wakelock=True
#orientation=all

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1


