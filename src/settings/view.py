#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from presenter import SettingsPresenter
from settings_repository import SettingsRepository

class SettingsView:
	def __init__(self):
		self.presenter = SettingsPresenter(self, SettingsRepository())

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
		self.gladefile = "settings.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		self.glade.connect_signals(self)
		self.liststore = self.glade.get_object('urls')
		self.treeView = self.glade.get_object('treeview')
		self.window = self.glade.get_object('settings')

	def update_feeds_list(self, settings):
		self.liststore.clear()
		for setting in settings:
			self._add_setting(setting)
		self.liststore.append([True, ""])
		self.treeView.set_model(self.liststore)
		self.show()

	def _add_setting(self, setting):
		self.liststore.append([True, setting.url])

	def _update_feed_settings(self, model, iter, column, new_text):
		row = model.get_string_from_iter(iter)
		self.presenter.update_setting(int(row), new_text)
