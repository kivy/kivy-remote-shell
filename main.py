__version__ = '0.1'

# install_twisted_rector must be called before importing  and using the reactor
#from kivy.support import install_twisted_reactor
#install_twisted_reactor()

import socket
import fcntl
import struct
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import App
from kivy.clock import Clock

from kivy.garden import navigationdrawer
from kivy.uix.screenmanager import Screen

from service import ServiceAppMixin
import twistedshell

app = None



class MainScreen(Screen):
    lan_ip = StringProperty('127.0.0.1')
    use_service = BooleanProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith('127.'):
            interfaces = ['eth0', 'eth1', 'eth2', 'wlan0', 'wlan1', 'wifi0',
                    'tiwlan0', 'tiwlan1', 'ath0', 'ath1', 'ppp0']
            for ifname in interfaces:
                try:
                    ip = self.get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        self.lan_ip = ip

    def get_interface_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])

    def on_use_service(self, instance, value):
        app.start_shell(service=value)


class RemoteKivyApp(App, ServiceAppMixin):
    def build(self):
        global app
        app = self

    def on_pause(self):
        return True

    def on_resume(self):
        return

    def on_stop(self):
        if hasattr(self, 'service'):
            self.stop_service()

    def start_shell(self, service=False):
        if service: # For now on, use the Service!
            if hasattr(self, '_twisted_connection'):
                twistedshell.uninstall_shell(service=False, connections=[self._twisted_connection])
                del self._twisted_connection
            self.start_service()

        else: # For now on, use the Activity!
            if hasattr(self, 'service'):
                self.stop_service()
            self._twisted_connection = twistedshell.install_shell(context=globals(), service=False)


if __name__ == '__main__':
    RemoteKivyApp().run()
