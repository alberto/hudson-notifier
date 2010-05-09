#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from presenter import SettingsPresenter
from settings_repository import SettingsRepository
import os

class SettingsView:
	def __init__(self):
		self.__dir_path = os.path.dirname(__file__)
		self.presenter = SettingsPresenter(self, SettingsRepository(self.__dir_path + '/config.txt'))

	def on_apply_clicked(self, treeView):
		self.presenter.save_prefs()
		gtk.Widget.destroy(self.window)

	def on_cancel_clicked(self, treeView):
		gtk.Widget.destroy(self.window)

	def on_url_edited(self, model, path, new_text):
		row = int(path)
		self.presenter.update_setting(row, new_text)

	def on_enabled_toggled(self, model, path):
		row = int(path)
		self.presenter.toggle_enabled(row)

	def open_prefs(self, widget, event, data = None):
		self.presenter.open_prefs()

	def show(self):
		self.window.show_all()

	def getUrls(self):
		return self.presenter.get_urls()

	def init_ui(self):
		SETTINGS_GLADE = os.path.abspath(self.__dir_path + '/../settings.glade')
		self.gladefile = SETTINGS_GLADE
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
		self.liststore.append([False, ""])
		self.treeView.set_model(self.liststore)
		self.show()

	def _add_setting(self, setting):
		self.liststore.append([setting.enabled, setting.url])
