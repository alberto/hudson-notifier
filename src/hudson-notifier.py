#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from notifier import Notifier
import gobject
import os

class HudsonNotifier:

	def __init__(self):
		dir_path = os.path.dirname(__file__)
		LOGO_IMG = os.path.abspath(dir_path + '/../imgs/logo.png')

		self.statusIcon = gtk.StatusIcon()
		self.statusIcon.set_from_file(LOGO_IMG)
		self.statusIcon.set_visible(True)
		self.statusIcon.set_tooltip("Hudson notifier")

		self.menu = gtk.Menu()
#    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
#    self.menuItem.connect('activate', self.prefs_cb, self.statusIcon)
#    self.menu.append(self.menuItem)
		self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
		self.menu.append(self.menuItem)

		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
		self.statusIcon.set_visible(1)
		self.notifier = Notifier()

		gobject.timeout_add(6000, self.poll)
		gtk.main()

	def getUrls(self):
		fileHandle = open('config.txt')
		return fileHandle.readlines()

	def poll(self):
		urls = self.getUrls()
		return self.notifier.poll(urls)

	def prefs_cb(self, widget, event, data = None):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_border_width(10)

		button = gtk.Button("Close")
		button.connect_object("clicked", gtk.Widget.destroy, window)
		window.add(button)
		button.show()
		window.show()

	def quit_cb(self, widget, data = None):
		gtk.main_quit()

	def popup_menu_cb(self, widget, button, time, data = None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
						3, time, self.statusIcon)

if __name__ == "__main__":
	helloWord = HudsonNotifier()

