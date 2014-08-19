from gi.repository import Gtk, GObject
from icons import *

class FriendList(Gtk.TreeView):

    def __init__(self):
        self.liststore = Gtk.ListStore(str, Gio.ThemedIcon)

        Gtk.TreeView.__init__(self, model=self.liststore)

        renderer = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.append_column(column_text)

        renderer = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Status", renderer, gicon=True)
        self.append_column(column_pixbuf)

    def update_from_roster(self,roster):
        self.liststore.clear()
        try:
            print("Appending roster")
            r = roster['matiaslina@gmail.com']
            for k in r:
                self.liststore.append([r[k]['name'], available_icon()])
        except RuntimeError as e:
            print(e)
            return False
        except TypeError:
            print("Roster is None")
        return True
