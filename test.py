__version__ = '0.2'

import socket
import fcntl
import struct
from twisted.internet import reactor
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh
from twisted.conch.ssh import keys
from twisted.conch.insults import insults

app = None

#+---[RSA 3072]----+
#|E .o o=.o.=..    |
#|o...=**=o= =     |
#|o.o.+*++= + . .  |
#|o+ . ....+ . o +.|
#|  o   ..S.  . . +|
#|       o ..      |
#|        .  .     |
#|         .  .    |
#|          ..     |
#+----[SHA256]-----+
private_rsa="""-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
"""

public_rsa="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCu2YF61scgIo8RABiwTvhZLmb0k2cdWaSKMn6yGdVbpAYtwbqZ6i9ZxOISrROLz+vtiPmg2DuCF42MoRyTlAlAkQs0iJVBDyIwM5mvACDCkvEqdCJhb5fgSgiqSVE9C+eDdIv24nZHPlD1OLfncivUIEPkn0SmwhSRjQt+IBeMB0yAzM4waci96m364SdJBHQ6YxjF2lFVMtWfqYFu80JZeklM+bmSwGAZ+QvLIt0sg4hcGci4voWu1EIf2SFbbxzHyjFyyzPl4Q4QRjZZXoJG5P6GmKdME9DPOpANtyRN80ZWpQs+VzjR4X1LBref1isolEvfY/1srfVlQZZYm7PLpdJnQP9Z2tkQb4NPMd7hB7yWLY5/sMrR1Fi8+PnrhAlYtG9AjOlSCMD/CRsCMmrWTILNlJ3ZZjFDPXvlQ1nNPuwdFcYeriSHs6hrnuj15tl/TESt6nXvyU6Dgwhys6UrkBmncclXweR8VDk/RQtVQA1zXnSmMKQ1fQCcbNYqTQM="

class PythonManhole(manhole.ColoredManhole):
    def __init__(self):
        glob = {
            '__name__':'__main__',
            '__doc__':None,
            '__package__':None,
            '__spec__':None,
            '__annotations__':{},
            '__builtins__':__builtins__
            }

        super().__init__(glob)

    def makeConnection(self, cxt):
        self.transport = cxt.transport
        return super().makeConnection(cxt)

    def lineReceived(self, *args):
        # Catch exit()
        try:
            return super().lineReceived(*args)
        except SystemExit:
            self.transport.loseConnection()


def getManholeFactory(**users):
    # Create a terminal
    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = PythonManhole
    users = {key: value.encode() for key, value in users.items()}
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))

    # Create a factory
    f = manhole_ssh.ConchFactory(p)
    f.publicKeys[b'ssh-rsa'] = keys.Key.fromString(public_rsa)
    f.privateKeys[b'ssh-rsa'] = keys.Key.fromString(private_rsa)
    return f


#class MainScreen:
#
#    def __init__(self, **kwargs):
#        ip = socket.gethostbyname(socket.gethostname())
#        if ip.startswith('127.'):
#            interfaces = ['eth0', 'eth1', 'eth2', 'wlan0', 'wlan1', 'wifi0',
#                    'tiwlan0', 'tiwlan1', 'ath0', 'ath1', 'ppp0']
#            for ifname in interfaces:
#                try:
#                    ip = self.get_interface_ip(ifname)
#                    break
#                except IOError:
#                    pass
#        self.lan_ip = ip
#
#    def get_interface_ip(self, ifname):
#        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        return socket.inet_ntoa(fcntl.ioctl(
#                s.fileno(),
#                0x8915,  # SIOCGIFADDR
#                struct.pack('256s', ifname[:15].encode('utf-8'))
#            )[20:24])
#
#
#
#    def on_pause(self):
#        return True

if __name__ == '__main__':
   # Define the local variables
   connection = reactor.listenTCP(8001, getManholeFactory(admin='kivy'))
   reactor.run()
