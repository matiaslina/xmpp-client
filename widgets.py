from gi.repository import Gtk, GObject
from icons import *
class TrayIcon(Gtk.StatusIcon):

    def __init__(self, icon):
        Gtk.StatusIcon.__init__(self)
        self.connect("popup-menu", self.on_right_click)
        self.set_from_gicon(icon)

    def on_right_click(self, icon, button, time):
        self.menu = Gtk.Menu()
 
        about = Gtk.MenuItem()
        about.set_label("About")
        quit = Gtk.MenuItem()
        quit.set_label("Quit")
 
        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", Gtk.main_quit)
 
        self.menu.append(about)
        self.menu.append(quit)
 
        self.menu.show_all()
 
        def pos(menu, icon):
            return (self.position_menu(menu, icon))
 
        self.menu.popup(None, None, pos, self, button, time)

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()
 
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("StatusIcon Example")
        about_dialog.set_version("0.0.1")
        about_dialog.set_authors(["Matias Linares"])
 
        about_dialog.run()
        about_dialog.destroy()


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
        r = roster['matiaslina@gmail.com']
        for k in r:
            print("name", r[k]['name'])
            self.liststore.append([r[k]['name'], available_icon()])

class ChatLayout(Gtk.Box):

    friend = ""
    def __init__(self, homogeneous=False, spacing=0,friend="Unknown", **kwds):
        
        print("init box")
        Gtk.Box.__init__(self,homogeneous, spacing, **kwds)

        self.friend = friend

        print("init scroll")
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        print("init textview")
        self.textview = Gtk.TextView()
        self.textview.get_buffer().set_text("")
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        print("Adding textview to scrollwindow")
        scrolledwindow.add(self.textview)

        print("Packing tha scrollwindow on the box")
        self.pack_start(scrolledwindow, True, True, 0)

        print("init entry")
        self.entry = Gtk.Entry()
        self.pack_start(self.entry, False, False, 0)

    def append_friend_text(self, new_msg):
        if not new_msg:
            return
        print("Getting textbuffer")
        text_buffer = self.textview.get_buffer()
        print("Textbuffer:", text_buffer)
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        print("text",text)
        new_text = "{}\n{}:{}".format(text, self.friend, new_msg)
        print(new_text)
        text_buffer.set_text(new_text)

