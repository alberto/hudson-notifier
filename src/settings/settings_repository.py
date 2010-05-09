#!/usr/bin/python
import pygtk
from hudson_feed_setting import HudsonFeedSetting
pygtk.require('2.0')

class SettingsRepository():
	def __init__(self, file):
		self.__file = file

	def get(self):
		settings = []
		try:
			fileHandle = open(self.__file)
			file_lines = fileHandle.readlines()
			for line in file_lines:
				setting = self.__get_setting(line)
				settings.append(setting)
			fileHandle.close()
		except IOError:
			pass
		finally:
			return settings

	def save(self, settings):
		fileHandle = open(self.__file, 'w')
		for feed_setting in settings:
			self.__save_setting(fileHandle, feed_setting)
		fileHandle.close()

	def __get_setting(self, line):
		line = line.replace('\n', '')
		if (line == ""):
			return
		return self._setting_from_format(line)

	def __save_setting(self, fileHandle, feed_setting):
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
