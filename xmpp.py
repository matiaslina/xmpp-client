import sleekxmpp
from mainwindow import MainWindow
from gi.repository import Gtk, Gdk, GLib
import threading

GTALK_SERVER = ('talk.google.com', 5222)
FACEBOOK_SERVER = ('chat.facebook.com', 5222)

class GtalkConnection(sleekxmpp.ClientXMPP):

    def __init__(self):
        with open("./.account", "r") as account_file:
            mail = account_file.readline()
            mail = mail[0:len(mail)-1]
            password = account_file.readline()
            password = password[0:len(password)-1]

        super(Connection, self).__init__(mail, password)
    
    def start_connection(self):
        self.connect()
        self.process(block=False)
