#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from notifier import Notifier
from preferences import Preferences
import gobject
import os

class HudsonNotifier:
	def __init__(self):
		self.setTrayApp()

		self.notifier = Notifier()
		gobject.timeout_add(6000, self.poll)
		gtk.main()

	def setTrayApp(self):
		dir_path = os.path.dirname(__file__)
		LOGO_IMG = os.path.abspath(dir_path + '/../imgs/logo.png')
		self.statusIcon = gtk.StatusIcon()
		self.statusIcon.set_from_file(LOGO_IMG)
		self.statusIcon.set_visible(True)
		self.statusIcon.set_tooltip("Hudson notifier")

		self.preferences = Preferences()

		self.menu = gtk.Menu()
		self.menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
		self.menuItem.connect('activate', self.preferences.open_prefs, self.statusIcon)
		self.menu.append(self.menuItem)
		self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
		self.menu.append(self.menuItem)

		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
		self.statusIcon.set_visible(1)

	def poll(self):
		urls = self.preferences.getUrls()
		return self.notifier.poll(urls)

	def quit_cb(self, widget, data = None):
		gtk.main_quit()

	def popup_menu_cb(self, widget, button, time, data = None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
						3, time, self.statusIcon)

if __name__ == "__main__":
	hn = HudsonNotifier()

