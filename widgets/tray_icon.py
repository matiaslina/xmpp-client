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
