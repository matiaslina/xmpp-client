from gi.repository import Gtk, Gio
from icons import *
import logging
import widgets
import xmpp
import os

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Xmpp client")
        self.set_border_width(3)
        self.set_default_size(200,400)

        self.setup_widgets()
        self.connect('delete-event', self.delete)
        self.show_all()

        self.connection = xmpp.Connection(self)
        self.connection.connect(xmpp.GTALK_SERVER)
        self.connection.process(block=False)

    def setup_widgets(self):
        hb = Gtk.HeaderBar()
        hb.props.title = "Xmpp client"
        hb.props.show_close_button = True
        self.set_titlebar(hb)

        button = Gtk.Button()
        image = Gtk.Image.new_from_gicon(settings_icon(), Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", lambda x: self.roster_updated())
        hb.pack_end(button)

        self.tray = widgets.TrayIcon(available_icon())
        self.tray.connect('activate', self._toggle_visibility)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        #self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(1000)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(False)
        scrolledwindow.set_vexpand(True)
        
        self.contact_list = widgets.FriendList()
        self.contact_list.connect('row-activated', self.row_activated_cb)
        #self.contact_list.connect('roster-updated', self._update_from_roster)

        scrolledwindow.add(self.contact_list)

        self.stack.add_titled(scrolledwindow, "contact list", "Contact_list")

        dummy_chat = widgets.ChatLayout(orientation=Gtk.Orientation.VERTICAL)
        self.stack.add_titled(dummy_chat, "chat", "Dummy Chat")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.pack_start(stack_switcher, False, False, 1)
        box.pack_start(self.stack, True, True, 1)

        self.add(box)

    def new_message_from_conn(self, friend, msg):
        print("msg from",friend,"saying", msg)

        # FIXME: this dies here :/ (maybe some problen with the gtk thread)
        if not self.stack.get_child_by_name(friend):
            print("Window Friend not found! Setting the stack")
            new_chat_window = widgets.ChatLayout(orientation=Gtk.Orientation.VERTICAL,friend=friend)
            new_chat_window.show_all()
            self.stack.add_titled(new_chat_window, friend, friend)
        else:
            print("Found")

        new_chat_window.append_friend_text(msg)
        child = self.stack.get_child_by_name(friend)
        self.stack.set_visible_child(child)
            
    def roster_updated(self):
        self.connection.get_roster()
        #self.conctact_list.emit('roster-updated', self.connection.get_roster())
        self.contact_list.update_from_roster(self.connection.roster)

    def delete(self, w, e):
        self.connection.disconnect(wait=True)
        Gtk.main_quit()

    def row_activated_cb(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        name = model.get_value(iter, 0)
        if not self.stack.get_child_by_name(name):
            new_chat_window = widgets.ChatLayout(orientation=Gtk.Orientation.VERTICAL)
            new_chat_window.show_all()
            self.stack.add_titled(new_chat_window, name, name)
        
        # Get the child and go to it
        child = self.stack.get_child_by_name(name)
        assert(child)
        self.stack.set_visible_child(child)

    def _toggle_visibility(self, w):
        if self.is_visible():
            self.set_visible(False)
        else:
            self.set_visible(True)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(levelname)-8s %(message)s')
    MainWindow()
    Gtk.main()
