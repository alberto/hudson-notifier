#!/usr/bin/python
import pygtk
from hudson_feed_setting import HudsonFeedSettingFactory
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
			setting = HudsonFeedSettingFactory().from_unicode_repr(line)
			settings.append(setting)
		return settings

	def save(self, settings):
		fileHandle = open('config.txt', 'w')
		for feed_setting in settings:
			self._save_setting(fileHandle, feed_setting)
		fileHandle.close()

	def _save_setting(self, fileHandle, feed_setting):
		fileHandle.write(feed_setting.__unicode__())
		fileHandle.write('\n')
