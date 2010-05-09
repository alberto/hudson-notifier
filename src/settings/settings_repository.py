#!/usr/bin/python
import pygtk
from hudson_feed_setting import HudsonFeedSettingFactory
from hudson_feed_setting import HudsonFeedSetting
pygtk.require('2.0')

class SettingsRepository():
	def get(self):
		fileHandle = open('config.txt')
		file_lines = fileHandle.readlines()
		settings = []
		for line in file_lines:
			line = line.replace('\n', '')
			if (line == ""):
				continue
			setting = self._setting_from_format(line)
			settings.append(setting)
		return settings

	def save(self, settings):
		fileHandle = open('config.txt', 'w')
		for feed_setting in settings:
			self._save_setting(fileHandle, feed_setting)
		fileHandle.close()

	def _save_setting(self, fileHandle, feed_setting):
		fileHandle.write(self._format_setting(feed_setting))
		fileHandle.write('\n')

	def _format_setting(self, feed_setting):
		return ("True" if feed_setting.enabled else "False") + '|' + feed_setting.url

	def _setting_from_format(self, formatted):
		bar = formatted.find("|")
		enabled = formatted[0:bar] == 'True'
		url = formatted[bar + 1:]
		setting = HudsonFeedSetting(url)
		setting.enabled = enabled
		return setting