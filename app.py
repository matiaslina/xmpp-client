from gi.repository import Gtk, Gdk, GObject
import logging

from mainwindow import MainWindow
import xmpp

class Application(object):

    def __init__(self):
        self.window = None
        self.connection = None

        self._init_window()

        self._init_connection()

        GObject.idle_add(self.send_data_to_gtk_thread)

    def _init_window(self):
        self.window = MainWindow()
        self.window.connect('delete-event', self.quit)

    def _init_connection(self):
        self.connection = xmpp.GtalkConnection()
        self.connection.start_connection()

    def send_data_to_gtk_thread(self):
        data = {
            'roster': '',
            'messages': [],
        }
        if self.connection.roster_changed and self.connection.roster != '':
            print("Updating roster")
            data["roster"] = self.connection.roster
        if self.connection.has_new_messages:
            print("adding messages")
            data["messages"] = self.connection.msg_queue

        if data:
            self.window.parse_new_data(data)
            self.connection.reset_data()

        return True

    def quit(self, widget, event):
        print("Exiting.. waiting disconnect form server") 
        self.connection.stop_connection()
        Gtk.main_quit()

def gtkmain():
    Gtk.main()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    app = Application()

    gtkmain()
    assert("We don't need to get here!")
