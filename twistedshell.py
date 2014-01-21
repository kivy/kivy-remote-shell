#coding: utf-8

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
    if not service:
        # install_twisted_rector must be called before importing  and using the reactor
        from kivy.support import install_twisted_reactor
        install_twisted_reactor()

    from twisted.internet import reactor

    print 'Creating twisted reactor'
    connection = reactor.listenTCP(8000,
        getManholeFactory(context, admin='kivy')
    )

    if service:
        # service-based have no implicit reactor running.
        print 'Twisted reactor starting'
        reactor.run()
        print 'Twisted reactor stopped'
    else:
        return connection
