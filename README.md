Kivy Remote Shell
=================

Remote SSH+Python interactive shell application. Great for having a remote
python shell on an embed platform like android.


Instructions
------------

* start the application
* connect to the ssh `ssh -p8000 admin@serverip`
* enter the password: kivy
* enjoy your python shell


Compile for android
-------------------

You must have setup http://github.com/kivy/python-for-android

```
$ git clone git://github.com/kivy/kivy-remote-shell
$ cd python-for-android
$ ./distribute.sh -m 'openssl pycrypto pyasn1 pyjnius twisted kivy'
$ cd dist/default
$ ./build.py --package org.kivy.sshshell --name "Kivy Remote Shell" \
  --version 1 --dir ../../../kivy-remote-shell/ \
  --icon ../../../kivy-remote-shell/icon.png --permission INTERNET debug installd
```

If you want to compile a release version for sharing, just replace `debug
installd` by `release`, and sign the APK!
