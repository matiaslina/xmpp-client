from gi.repository import Gtk, Gdk, GObject
import logging

from mainwindow import MainWindow
import xmpp

class Application(object):

    def __init__(self):
        self.window = None
        self.connection = None
        self.data = {
            "roster": {
                "data": None,
                "changed": True
            },
            "msg_queue": [],
        }
        self._init_window()

        self._init_connection()

        GObject.idle_add(self.send_data_to_gtk_thread)

    def _init_window(self):
        self.window = MainWindow()
        self.window.connect('delete-event', self.quit)

    def _init_connection(self):
        self.connection = xmpp.Connection()
        self.connection.start_connection()

        self.connection.add_event_handler('session_start', self.start)

        self.connection.add_event_handler('message', self.on_new_message)


    def on_new_message(self, msg):
        self.data["msg_queue"].append(msg)
        return False

    def start(self, event):
        print("sending presence")
        self.connection.send_presence()
        self.connection.get_roster()
        return False

    def roster_update(self):
        if self.data["roster"]["data"] != None and self.data["roster"]["data"] == self.connection.roster:
            self.data["roster"]["changed"] = False
        else:
            self.data["roster"]["changed"] = True
            self.data["roster"]["data"] = self.connection.roster

    def send_data_to_gtk_thread(self):
        self.roster_update()
        self.window.parse_new_data(self.data)
        return True

    def quit(self, widget, event):
        print("Exiting.. waiting disconnect form server") 
        self.connection.disconnect(wait=True)
        Gtk.main_quit()

def gtkmain():
    Gtk.main()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(levelname)-8s %(message)s')

    app = Application()

    gtkmain()
    assert("We don't need to get here!")
