#!/usr/bin/python
import pygtk
from hudson_feed_setting import HudsonFeedSetting
pygtk.require('2.0')

class SettingsPresenter():
	def __init__(self, view, repository):
		self.view = view
		self.repository = repository
		self.model = repository.get()

	def save_prefs(self):
		self.repository.save(self.model)

	def open_prefs(self):
		self.view.init_ui()
		self.model = self.repository.get()
		self.view.update_feeds_list(self.model)
		self.view.show()

	def update_setting(self, row, url):
		if (len(self.model) == row):
			if (url != ""):
				self.model.append(HudsonFeedSetting(url))
		elif (url == ""):
			self.model.pop(row)
		else:
			self.model[row] = HudsonFeedSetting(url)
		self.view.update_feeds_list(self.model)

	def toggle_enabled(self, row):
		if (row >= len(self.model)):
			return
		self.model[row].enabled = not self.model[row].enabled
		self.view.update_feeds_list(self.model)

	def get_urls(self):
		settings = self.repository.get()
		enabled_settings = filter(lambda x: x.enabled, settings)
		return map(lambda x: x.url, enabled_settings)

	def get_number_of_elements(self):
		return len(self.model)
