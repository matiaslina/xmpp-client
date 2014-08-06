import sleekxmpp
from mainwindow import MainWindow
from gi.repository import Gtk, Gdk, GLib
import threading

GTALK_SERVER = ('talk.google.com', 5222)
FACEBOOK_SERVER = ('chat.facebook.com', 5222)

class Connection(sleekxmpp.ClientXMPP):

    def __init__(self):
        with open("./.account", "r") as account_file:
            mail = account_file.readline()
            mail = mail[0:len(mail)-1]
            password = account_file.readline()
            password = password[0:len(password)-1]
        super(Connection, self).__init__(mail, password)

        self.add_event_handler('session_start', self.start)
        Gdk.threads_enter()
        self.window = MainWindow()
        self.window.connect('delete-event', self.quit)
        self.window.contact_button.connect("clicked",
                                           lambda x: self.manual_roster_update())
        Gdk.threads_leave()

        self.add_event_handler('message', self.on_new_message)

    def on_new_message(self, msg):
        self.window.new_message(msg)
        while Gtk.events_pending():
            print("pending")
            Gtk.main_iteration()
        print("done")
        return False

    def start(self, event):
        print("sending presence")
        self.send_presence()
        self.get_roster()

    def manual_roster_update(self):
        self.window.contact_list.update_from_roster(self.roster)

    def quit(self, w, e):
        self.disconnect(wait=True)
        Gtk.main_quit()

def gtkmain():
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()

if __name__ == "__main__":
    GLib.threads_init()
    Gdk.threads_init()

    conn = Connection()
    conn.connect(GTALK_SERVER)
    conn.process(block=False)

    #t = threading.Thread(target=gtkmain)
    #t.start()
    gtkmain()
    assert("We don't need to get here!")
