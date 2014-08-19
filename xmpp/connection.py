import sleekxmpp
from mainwindow import MainWindow
from gi.repository import Gtk, Gdk, GLib
import threading

GTALK_SERVER = ('talk.google.com', 5222)
FACEBOOK_SERVER = ('chat.facebook.com', 5222)

class GtalkConnection(sleekxmpp.ClientXMPP):

    def __init__(self):
        self.old_roster = None
        self.roster_changed = False
        self.has_new_messages = False
        self.msg_queue = []

        with open("./.account", "r") as account_file:
            mail = account_file.readline()
            self.mail = mail[0:len(mail)-1]
            password = account_file.readline()
            password = password[0:len(password)-1]

        super(GtalkConnection, self).__init__(self.mail, password)

    # Start and stop the server
    
    def start_connection(self):
        self.connect(GTALK_SERVER)
        self.process(block=False)
        self.add_event_handler('session_start', self._session_start_cb)
        self.add_event_handler('message', self._on_message_cb)
        self.add_event_handler('roster_update', self._roster_update_cb)

    def stop_connection(self):
        self.disconnect(wait=True)

    # Callbacks

    def _session_start_cb(self, event):
        print("sending presence")
        self.send_presence()
        self.get_roster()

        return False

    def _on_message_cb(self, msg):
        print("Message received")
        self.has_new_messages = True
        try:
            mail = str(msg["from"]).split("/")[0]
            name = dict(self.roster[self.mail]).get(mail)["name"]
            print("appending {}".format({'from': name, 'msg': msg}))
            self.msg_queue.append({'from': name, 'msg': msg})
        except Exception as e:
            print("ERROR")
            print(e)
        return False

    def _roster_update_cb(self, roster):
        print("Roster Changed")
        self.roster_changed = True
        self.old_roster = self.roster
        return False
    
    def reset_data(self):
        self.roster_changed = False
        self.has_new_messages = False
        del self.msg_queue[:]

    def send_msg_to(self, to, msg):
        print("Calling send msg")
        self.send_msg(mto=to, mbody=msg, mtype='chat')
