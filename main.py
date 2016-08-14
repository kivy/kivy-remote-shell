__version__ = '0.1'

# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

import socket
import fcntl
import struct
from twisted.internet import reactor
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.app import App

from kivy.garden import navigationdrawer
from kivy.uix.screenmanager import Screen
app = None


def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    def getManhole(_):
        return manhole.ColoredManhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f


class MainScreen(Screen):
    lan_ip = StringProperty('127.0.0.1')

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


class RemoteKivyApp(App):
    def build(self):
        global app
        app = self
        self.connection = reactor.listenTCP(8000,
                getManholeFactory(globals(), admin='kivy'))

    def on_pause(self):
        return True

if __name__ == '__main__':
    RemoteKivyApp().run()
