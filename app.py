from gi.repository import Gtk, Gdk, GObject
import logging

from mainwindow import MainWindow
from xmpp.connection import GtalkConnection

def dict_have_data(d):
    """
        returns if a dict has (non empty) data in it
    """
    retval = False
    for _,v in d.items():
        retval = bool(retval or v)

    return retval

class Application(object):

    def __init__(self):
        self.window = None
        self.connection = None

        self._init_window()

        self._init_connection()

        GObject.idle_add(self.send_data_to_gtk_thread)
        #GObject.idle_add(self.retrieve_data_from_gtk)

    def _init_window(self):
        self.window = MainWindow()
        self.window.connect('delete-event', self.quit)

    def _init_connection(self):
        self.connection = GtalkConnection()
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

        if dict_have_data(data):
            self.window.parse_new_data(data)
            self.connection.reset_data()

        return True

    def retrieve_data_from_gtk(self):
        to, client_data = self.window.get_send_data()
        if client_data != None:
            for msg in client_data:
                print("sending msg",msg)
                self.connection.send_msg_to(to, msg)

        return False


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
