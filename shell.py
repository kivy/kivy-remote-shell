#coding: utf-8
from threading import Lock
from kivy.logger import Logger

INSTALL_SHELL_LOCK = Lock()


def _block_on(d, timeout=None):
    '''Blocks waiting for a deferred to return something, or fail'''
    from Queue import Queue, Empty
    from twisted.python.failure import Failure

    q = Queue()
    d.addBoth(q.put)
    try:
        ret = q.get(True, timeout)
    except Empty:
        raise Empty
    if isinstance(ret, Failure):
        ret.raiseException()
    else:
        return ret


def getManholeFactory(namespace, **passwords):
    from twisted.cred import portal, checkers
    from twisted.conch import manhole, manhole_ssh

    realm = manhole_ssh.TerminalRealm()
    def getManhole(_):
        return manhole.ColoredManhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f


def install_shell(context={}, service=False):
    with INSTALL_SHELL_LOCK:
        if service:
            from twisted.internet import default
            default.install()
        else:
            # install_twisted_rector must be called before importing  and using the reactor
            from kivy.support import install_twisted_reactor
            install_twisted_reactor()

        from twisted.internet import reactor

        Logger.debug('Shell: Creating twisted reactor. Service: %s', service)
        connection = reactor.listenTCP(8001,
            getManholeFactory(context, admin='kivy')
        )

        if service:
            # service-based have no implicit reactor running.
            Logger.debug('Shell: Twisted reactor starting')
            reactor.run()
            Logger.debug('Shell: Twisted reactor stopped')
        else:
            return connection

def uninstall_shell(service=False, connections=[]):
    if service:
        raise NotImplementedError()

    defers = []
    for c in connections:
        defers.append(c.stopListening())

    from Queue import Empty
    import kivy.support
    while True:
        kivy.support._twisted_reactor_work()
        try:
            for d in defers:
                _block_on(d, timeout=1)
        except Empty:
            continue
        break

    from kivy.support import uninstall_twisted_reactor
    uninstall_twisted_reactor()
