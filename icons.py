from gi.repository import Gio

def settings_icon():
    return Gio.ThemedIcon(name="preferences-system-symbolic")

def list_icon():
    return Gio.ThemedIcon(name="view-sidebar-symbolic")

def available_icon():
    return Gio.ThemedIcon(name="user-available-symbolic")

def away_icon():
    return Gio.ThemedIcon(name="user-away-symbolic")

def busy_icon():
    return Gio.ThemedIcon(name="user-busy-symbolic")

def offline_icon():
    return Gio.ThemedIcon(name="user-offline-symbolic")

