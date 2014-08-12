from gi.repository import Gtk, GObject
from icons import *

class FriendList(Gtk.TreeView):
    """
    __gsignals__ = {
        'roster-updated': (
            GObject.SIGNAL_RUN_FIRST,   # When
            None,                       # Return (always none)
            (dict,)                     # parameters
        )
    }
    """


    def __init__(self):
        self.liststore = Gtk.ListStore(str, Gio.ThemedIcon)
        self.liststore.append(["some", available_icon()])
        self.liststore.append(["other", away_icon()])
        self.liststore.append(["waaaaa", available_icon()])

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
