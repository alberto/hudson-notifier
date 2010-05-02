#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import gobject

class Preferences:
	def __init__(self):
		return
	def open_prefs(self, widget, event, data = None):
		self.gladefile = "preferences.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		self.glade.connect_signals(self)

		self.create_model()
		treeView = self.glade.get_object('treeview')
		treeView.set_model(self.liststore)
		self.window = self.glade.get_object('preferences')
		self.window.show_all()

	def getUrls(self):
		fileHandle = open('config.txt')
		return fileHandle.readlines()

	def create_model(self):
		self.liststore = gtk.ListStore(gobject.TYPE_BOOLEAN, str)
		for act in self.getUrls():
			self.liststore.append([True, act])

	def on_add_clicked(self, treeView):
		print "add clicked"

	def on_close_clicked(self, treeView):
		gtk.Widget.destroy(self.window)

if __name__ == "__main__":
	pref = Preferences()
	pref.open_prefs(None, None, None)
	gtk.main()
