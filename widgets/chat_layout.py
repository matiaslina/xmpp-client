from gi.repository import Gtk, GObject
from icons import *

class ChatLayout(Gtk.Box):

    def __init__(self, homogeneous=False, spacing=0,friend="Unknown", email=None, **kwds):

        self.friend = friend
        self.email = email
        self.send_msg = []
        
        Gtk.Box.__init__(self,homogeneous, spacing, **kwds)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        self.textview = Gtk.TextView()
        self.textview.get_buffer().set_text("")
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        scrolledwindow.add(self.textview)

        self.pack_start(scrolledwindow, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.entry_activate_cb)
        self.pack_start(self.entry, False, False, 0)

    def append_friend_text(self, new_msg):
        if not new_msg:
            return
        text_buffer = self.textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        new_text = "{}\n{}:{}".format(text, self.friend, new_msg)
        text_buffer.set_text(new_text)

    def append_my_text(self, new_msg):
        if not new_msg:
            return
        text_buffer = self.textview.get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), True)
        new_text = "{}\nMe:{}".format(text, new_msg)
        text_buffer.set_text(new_text)

    def entry_activate_cb(self, w):
        text = self.entry.get_text()
        if text != "":
            self.send_msg.append(self.entry.get_text())
            self.append_my_text(text)
            self.entry.set_text("")

        print(self.send_msg)

    def has_messages(self):
        return len(self.send_msg) > 0

    def clear_messages(self):
        del self.send_msg[:]
