.. _top:

Command list
============

   -  TTS_
   -  GPS_
   -  NOTIFICATION_
   -  SMS_
   -  COMPASS_
   -  VIBRATION_
   -  UNIQID_
   -  FLASH_
   -  CAMERA_
   -  EMAIL_
   -  BATTERY_
   -  ACCELERATOR_
   -  GYROSCOPE_
   -  CALL_
   
TTS(Text to speech)
-------------------

Example::

    from plyer import tts
    tts.speak('text')

top_

GPS
---

.. _GPS:

.. note::

   This will work only on versions before android 6.0 .
   
   For android 6.0 + the coder needs to explictly ask permissions.


Here is an example of the usage of gps::

    from plyer import gps
    coordinate = 0
    def print_locations(**kwargs):
        global coordinate
        coordinate = kwargs
        
    gps.configure(on_location=print_locations)
    gps.start()
    # later
    print coordinate
    gps.stop()


Notification
------------

.. _NOTIFICATION:

Example::

    from plyer import notification
    notication.notify('Text')

SMS
---

.. _SMS:

Example::

    from plyer import sms
    sms.send(recipient=self.sms_recipient, message=self.sms_message)

Uniqueid
--------

.. _UNIQID:

Example::

    from plyer import uniqueid
    uniqueid.id


vibrator
--------

.. _VIBRATION:

Example::

    from plyer import vibrator
    vibrator.vibrate(10)

Compass
-------

.. _COMPASS:

Example::

    from plyer import compass
    compass.enable()
    compass.orientation
    compass.disable()

Flash
-----

.. _FLASH:

Example::

    from plyer import flash
    flash.on()
    flash.off()


camera
------

.. _CAMERA:

Example::

    from plyer import camera
    camera.take_picture

E-Mail
------

.. _EMAIL:

Example::

    from plyer import email
    email.send(recipient='abc@gmail.com', subject='Message')

Call
----

.. _CALL:

Example::

    from plyer import call
    call.makecall('9013159973')


Accelerometer
-------------

.. _ACCELERATOR:

Example::

    from plyer import accelerometer
    accelerometer.enable()
    accelerator.acceleration

Battery
--------

.. _BATTERY:

Example::

    from plyer import battery
    battery.status

Gyroscope
---------

.. _GYROSCOPE:

Example::

    from plyer import gyroscope
    gyroscope.enable()
    gyroscope.orientation
    gyroscope.disable()

Orientation
-----------

Example::

    from plyer import orientation
    orientation.set_landscape()
    orientation.set_portrait()

Audio
-----

Example::

    from plyer import audio


IrBlaster
---------

Example::

    from plyer import irblaster

