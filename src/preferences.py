#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import gobject

class Preferences:
	def __init__(self):
		self.load_ui()
		self.create_model()

	def load_ui(self):
		self.gladefile = "preferences.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		self.glade.connect_signals(self)
		self.liststore = self.glade.get_object('urls')

	def open_prefs(self, widget, event, data = None):
		self.load_ui()
		self.create_model()
		self.treeView = self.glade.get_object('treeview')
		self.treeView.set_model(self.liststore)
		self.window = self.glade.get_object('preferences')
		self.window.show_all()

	def getUrls(self):
		urls = []
		for entry in self.liststore:
			if not entry[0]:
				continue
			urls.append(entry[1])
		return urls

	def load_prefs(self):
		fileHandle = open('config.txt')
		file_lines = fileHandle.readlines()
		return [line.replace('\n', '') for line in file_lines]

	def create_model(self):
		for act in self.load_prefs():
			self.liststore.append([True, act])

	def on_add_clicked(self, button):
		self.liststore.append([True, ""])
		self.focus_on_last_row()

	def focus_on_last_row(self):
		row = len(self.liststore) - 1
		column = self.treeView.get_column(1)
		self.treeView.set_cursor(row, column, True)

	def on_apply_clicked(self, treeView):
		self.save_prefs()
		gtk.Widget.destroy(self.window)

	def on_cancel_clicked(self, treeView):
		gtk.Widget.destroy(self.window)

	def save_prefs(self):
		fileHandle = open('config.txt', 'w')
		for config in self.liststore:
			fileHandle.write(config[1])
			fileHandle.write('\n')
		fileHandle.close()

	def on_enabled_toggled(self, model, path):
		iter = model.get_iter_from_string(path)
		model.set_value(iter, 0, not model.get_value(iter, 0))

	def on_url_edited(self, model, path, new_text):
		iter = model.get_iter_from_string(path)
		model.set_value(iter, 1, new_text)

if __name__ == "__main__":
	pref = Preferences()
	pref.open_prefs(None, None, None)
	gtk.main()
