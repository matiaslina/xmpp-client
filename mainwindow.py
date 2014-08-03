from gi.repository import Gtk, Gio, GObject
from gi.repository import Gdk, GLib
from icons import *
import logging
import widgets
import os


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Xmpp client")
        self.set_border_width(3)
        self.set_default_size(200,400)

        self.setup_header()
        self.setup_widgets()
        self.show_all()

    def setup_header(self):
        hb = Gtk.HeaderBar()
        hb.props.title = "Xmpp client"
        hb.props.show_close_button = True
        self.set_titlebar(hb)

        self.contact_button = Gtk.Button()
        image = Gtk.Image.new_from_gicon(list_icon(), Gtk.IconSize.BUTTON)
        self.contact_button.add(image)
        hb.pack_start(self.contact_button)

        self.settings_button = Gtk.Button()
        image = Gtk.Image.new_from_gicon(settings_icon(), Gtk.IconSize.BUTTON)
        self.settings_button.add(image)
        hb.pack_end(self.settings_button)

        self.settings_popover = Gtk.Popover.new(self.settings_button)
        self.settings_popover.add(Gtk.Label("hola"))
        self.settings_button.connect('clicked', self.settings_on_click)

    def settings_on_click(self, widget):
        if self.settings_popover.get_visible():
            self.settings_popover.hide()
        else:
            self.settings_popover.show_all()

    def setup_widgets(self):
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

        scrolledwindow.add(self.contact_list)

        self.stack.add_titled(scrolledwindow, "contact list", "Contact_list")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.pack_start(stack_switcher, False, False, 1)
        box.pack_start(self.stack, True, True, 1)

        self.add(box)

    def new_message(self, msg):
        print("MSG!")
        print("tyoe", msg["type"])
        print("Guard:",msg['type'] in ('chat', 'normal') )
        if msg['type'] in ('chat', 'normal'):
            self.new_message_from_conn(str(msg['from']),str(msg['body']))
        else:
            print("[XMPP] Not chat or normal - ", msg['body'])

    def new_message_from_conn(self, friend, msg):
        """
        friend and msg *needs* to be strings @ this point
        Gdk.threads_enter/leave() don't work here, the app hangs :/
        """
        print("new_msg signal activated with friend",friend,"and msg",msg)

        Gdk.threads_enter()
        if not self.stack.get_child_by_name(friend):
            print("Window Friend not found! Setting the stack")
            new_chat_window = widgets.ChatLayout(orientation=Gtk.Orientation.VERTICAL,friend=friend)
            print("show_all()")
            new_chat_window.show_all()
            print("add_titled(...)")
            self.stack.add_titled(new_chat_window, friend, friend)
        else:
            print("Found")

        print("get_child")
        child = self.stack.get_child_by_name(friend)
        print("set_visible_child")
        self.stack.set_visible_child(child)
        #new_chat_window.append_friend_text(msg)
        print("leving threads")
        Gdk.threads_leave()
        print("outside thread")

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
    w = MainWindow()
    w.connect('destroy', Gtk.main_quit)
    Gtk.main()
