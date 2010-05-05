#!/usr/bin/python
import pygtk
from hudson_feed_setting import HudsonFeedSetting, HudsonFeedSettingFactory
pygtk.require('2.0')

class PreferencesPresenter():
	def __init__(self, view):
		self.view = view
		self.model = self._load_settings()

	def save_prefs(self):
		fileHandle = open('config.txt', 'w')
		for feed_setting in self.model:
			self._save_setting(fileHandle, feed_setting)
		fileHandle.close()

	def _save_setting(self, fileHandle, feed_setting):
		fileHandle.write(feed_setting.__unicode__())
		fileHandle.write('\n')

	def open_prefs(self):
		self.view.init_ui()
		self.model = self._load_settings()
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

	def _load_settings(self):
		fileHandle = open('config.txt')
		file_lines = fileHandle.readlines()
		lines = []
		for line in file_lines:
			line = line.replace('\n', '')
			if (line == ""):
				continue
			setting = HudsonFeedSettingFactory().from_unicode_repr(line)
			lines.append(setting)
		return lines

	def get_urls(self):
		return self.model

	def get_number_of_elements(self):
		return len(self.model)
