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


```
$ pip install buildozer --user
$ git clone git://github.com/kivy/kivy-remote-shell
$ cd kivy-remote-shell
$ pip install -r requirements.txt
$ buildozer android_new debug deploy run logcat
```

Pre-built debug apk available at http://bit.ly/KivyRemote2


If you want to compile a release version for sharing, just replace `debug
installd` by `release`, and sign the APK!
