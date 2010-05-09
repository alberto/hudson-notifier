#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from poller_factory import PollerFactory
from settings.view import SettingsView
import gobject
import os

class HudsonNotifierUI:
	def __init__(self):
		self.settings_view = SettingsView()
		self.poller = PollerFactory().get()
		self.configure_ui()
		gobject.timeout_add(100, self.poll_first_time)
		gobject.timeout_add(60000, self.poll)
		gtk.main()

	def configure_ui(self):
		dir_path = os.path.dirname(__file__)
		MAIN_GLADE = os.path.abspath(dir_path + '/main.glade')
		self.gladefile = MAIN_GLADE
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)

		self.statusIcon = self.glade.get_object('tray_icon')
		LOGO_IMG = os.path.abspath(dir_path + '/../imgs/logo.png')
		self.statusIcon.set_from_file(LOGO_IMG)
		self.connect_events()

	def connect_events(self):
		self.menu = self.glade.get_object('menu')
		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)

		self.menuItem = self.glade.get_object('settings')
		self.menuItem.connect('activate', self.settings_view.open_prefs, self.statusIcon)

		self.menuItem = self.glade.get_object('quit')
		self.menuItem.connect('activate', self.on_quit_activate, self.statusIcon)

	def poll_first_time(self):
		self.poll()
		return False

	def poll(self):
		urls = self.settings_view.getUrls()
		return self.poller.poll(urls)

	def on_quit_activate(self, widget, data = None):
		gtk.main_quit()

	def popup_menu_cb(self, widget, button, time, data = None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
						3, time, self.statusIcon)

if __name__ == "__main__":
	hn = HudsonNotifierUI()
