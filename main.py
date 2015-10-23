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

app = None

Builder.load_string('''
<MainScreen>:
    Image:
        source: 'background.png'
        allow_stretch: True
        keep_ratio: False
    BoxLayout:
        size_hint_y: .2
        pos_hint: {'top': 1}
        canvas:
            Color:
                rgba: .1, .1, .1, .1
            Rectangle:
                pos: self.pos
                size: self.size
        Widget
        Image:
            source: 'icon.png'
            mipmap: True
            size_hint_x: None
            width: 100
        Label:
            text: 'Remote Kivy'
            font_size: 30
            size_hint_x: None
            width: self.texture_size[0] + 20
        Widget
    Label:
        text: 'ssh -p8000 admin@{0}'.format(root.lan_ip)
        font_size: 20
        size_hint_y: .8
''')

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


class MainScreen(FloatLayout):
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
        return MainScreen()

    def on_pause(self):
        return True

    def on_resume(self):
        return True

if __name__ == '__main__':
    RemoteKivyApp().run()
