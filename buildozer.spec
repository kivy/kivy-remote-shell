[app]

# title of the application
title = Kivy Remote Shell

# package name
package.name = remoteshell

# package domain (mostly used for android/ios package)
package.domain = org.kivy

# indicate where the source code is living
source.dir = .
source.include_exts = py,png

# search the version information into the source code
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# requirements of the app
requirements = pycrypto,pyasn1,pyjnius,twisted,kivy

# android specific
android.permissions = INTERNET

