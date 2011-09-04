#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

__author__ = "amrut.joshi@gmail.com"
__version__ = "0.1"

import warnings
warnings.simplefilter('ignore', DeprecationWarning)

import sys
import xmpp
import getpass
import select
import cleverbot

def main():
    cb = cleverbot.Session()

    def xmpp_message(self, event):
        msg = event.getBody()
        frm = event.getAttr("from")
        print "%s: %s" % (frm, msg)
        ans = cb.Ask(msg)
        ans = ans.split("}")[-1]
        self.send(xmpp.Message(frm, ans))
        print "You: %s" % ans

    login = raw_input("Login (without '@gmail.com'): ")
    passwd = getpass.getpass()
    cl = xmpp.Client('gmail.com', debug=[])
    cl.connect(server = ('talk.google.com', 5222))
    cl.auth(login, passwd, 'botty')
    cl.RegisterHandler('message', xmpp_message)
    cl.sendInitPresence(requestRoster=0)   # you may need to uncomment this for old server

    socketlist = {cl.Connection._sock:'xmpp'}
    online = 1

    while online:
        (i, o, e) = select.select(socketlist.keys(),[],[],0)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            else:
                raise Exception("Unknown socket type: ")




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
