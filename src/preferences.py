#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk

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
		lines = [line.replace('\n', '') for line in file_lines]
		if len(lines) == 0 or lines[-1] != "":
			lines.append("")
		return lines

	def create_model(self):
		for act in self.load_prefs():
			self.liststore.append([True, act])

	def focus_on_last_row(self):
		row = self._get_index_of_last_row()
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
		self.update_model(model, iter, 1, new_text)

	def update_model(self, model, iter, column, new_text):
		last_row = str(self._get_index_of_last_row())
		row = model.get_string_from_iter(iter)
		if (row != last_row and new_text == ""):
			model.remove(iter)
			self.treeView.set_model(model)
			return

		if (row == last_row and new_text != ""):
			self.liststore.append([True, ""])
		model.set_value(iter, 1, new_text)

	def _get_number_of_elements(self):
		return len(self.liststore)

	def _get_index_of_last_row(self):
		return self._get_number_of_elements() - 1

if __name__ == "__main__":
	pref = Preferences()
	pref.open_prefs(None, None, None)
	gtk.main()
