#!/usr/bin/python

class HudsonFeedSetting():
	def __init__(self, url):
		self.enabled = True
		self.url = url

	def __unicode__(self):
		return self.url

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self.__str__()

	def from_unicode_repr(self, string):
		self.url = string

class HudsonFeedSettingFactory():
	def from_unicode_repr(self, string):
		return HudsonFeedSetting(string)
