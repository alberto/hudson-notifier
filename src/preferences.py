#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk

class Preferences:
	def __init__(self):
		self.presenter = Presenter(self)

	def on_apply_clicked(self, treeView):
		self.presenter.save_prefs()
		gtk.Widget.destroy(self.window)

	def on_cancel_clicked(self, treeView):
		gtk.Widget.destroy(self.window)

	def on_url_edited(self, model, path, new_text):
		iter = model.get_iter_from_string(path)
		self._update_feed_settings(model, iter, 1, new_text)

	def open_prefs(self, widget, event, data = None):
		self.presenter.open_prefs()

	def show(self):
		self.window.show_all()

	def getUrls(self):
		return self.presenter.get_urls()

	def init_ui(self):
		self.gladefile = "preferences.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		self.glade.connect_signals(self)
		self.liststore = self.glade.get_object('urls')
		self.treeView = self.glade.get_object('treeview')
		self.window = self.glade.get_object('preferences')

	def update_feeds_list(self, settings):
		self.liststore.clear()
		for setting in settings:
			self._add_setting(setting)
		self._add_setting("")
		self.treeView.set_model(self.liststore)
		self.show()

	def _add_setting(self, setting):
		self.liststore.append([True, setting])

	def _update_feed_settings(self, model, iter, column, new_text):
		row = model.get_string_from_iter(iter)
		self.presenter.update_setting(int(row), new_text)

class Presenter():
	def __init__(self, view):
		self.view = view
		self.model = self._load_prefs()

	def save_prefs(self):
		fileHandle = open('feed_setting.txt', 'w')
		for feed_setting in self.model:
			self._save_setting(fileHandle, feed_setting)
		fileHandle.close()

	def _save_setting(self, fileHandle, feed_setting):
		fileHandle.write(feed_setting[1])
		fileHandle.write('\n')

	def open_prefs(self):
		self.view.init_ui()
		self.model = self._load_prefs()
		self.view.update_feeds_list(self.model)
		self.view.show()

	def update_setting(self, row, url):
		if (len(self.model) == row):
			if (url != ""):
				self.model.append(url)
		elif (url == ""):
			self.model.pop(row)
		else:
			self.model[row] = url
		self.view.update_feeds_list(self.model)

	def _load_prefs(self):
		fileHandle = open('config.txt')
		file_lines = fileHandle.readlines()
		lines = []
		for line in file_lines:
			line = line.replace('\n', '')
			if (line == ""):
				continue
			lines.append(line)
		return lines

	def get_urls(self):
		return self.model

	def get_number_of_elements(self):
		return len(self.model)

#class HudsonFeed():
#	def __init__(self):
#		self.url = ""
