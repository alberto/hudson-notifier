#!/usr/bin/env python
import feedparser
import pynotify
import os

class Notifier():
	BASE_TITLE = 'Hudson Update'
	TIMEOUT = 1000
	dir_path = os.path.dirname(__file__)
	SUCCESS_IMG = os.path.abspath(dir_path + '/../imgs/success.png')
	UNSTABLE_IMG = os.path.abspath(dir_path + '/../imgs/unstable.png')
	FAILURE_IMG = os.path.abspath(dir_path + '/../imgs/failure.png')

	def __init__(self):
		self.last_displayed = dict()
		pynotify.init('Hudson Notifier')

	def success(self, job, build):
		n = pynotify.Notification(self.BASE_TITLE,
	'"%s"  %s successfully built.' % (job, build),
		self.SUCCESS_IMG)
		n.set_urgency(pynotify.URGENCY_LOW)
		n.set_timeout(self.TIMEOUT)
		return n

	def unstable(self, job, build):
		n = pynotify.Notification(self.BASE_TITLE,
		'"%s" %s is unstable.' % (job, build),
		self.UNSTABLE_IMG)
		n.set_timeout(self.TIMEOUT)
		return n

	def failure(self, job, build):
		n = pynotify.Notification(self.BASE_TITLE,
		'"%s" %s failed!' % (job, build),
		self.FAILURE_IMG)
		n.set_urgency(pynotify.URGENCY_CRITICAL)
		n.set_timeout(self.TIMEOUT)
		return n

	def poll(self, urls):
		for url in urls:
			feed = feedparser.parse(url)
			items = [t['title'] for t in feed['entries']]
			for i in items:
				i = i.split(' ')
				job, build, status = (i[0], i[1], i[2])

				if job in self.last_displayed and self.last_displayed[job] == (build, status):
					continue
				self.last_displayed[job] = (build, status)
				status = status.replace('(', '').replace(')', '')
				if status == 'SUCCESS':
					self.success(job, build).show()
				elif status == 'UNSTABLE':
					self.unstable(job, build).show()
				elif status == 'FAILURE':
					self.failure(job, build).show()
		return True
