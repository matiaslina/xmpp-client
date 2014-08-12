from gi.repository import Gtk, GObject
from icons import *

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

