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

	statuses = {
		'success' : [ '"%s" %s successfully built.', SUCCESS_IMG, pynotify.URGENCY_LOW],
		'unstable' : [ '"%s" %s is unstable.', UNSTABLE_IMG, pynotify.URGENCY_NORMAL],
		'failure' : [ '"%s" %s failed!', FAILURE_IMG, pynotify.URGENCY_CRITICAL]
	}

	def __init__(self):
		self.last_displayed = dict()
		pynotify.init('Hudson Notifier')

	def notify(self, job, build, status):
		status_values = self.statuses[status]
		n = pynotify.Notification(
			self.BASE_TITLE,
			status_values[0] % (job, build),
			status_values[1])
		n.set_urgency(status_values[2])
		n.set_timeout(self.TIMEOUT)
		return n

	def poll(self, urls):
		for url in urls:
			feed = feedparser.parse(url)
			items = [t['title'] for t in feed['entries']]
			for item in items:
				build, job, status = self._get_build_info(item)
				if self._is_old_build(job, build, status):
					continue
				self.last_displayed[job] = (build, status)
				self.notify(job, build, status).show()
		return True

	def _get_build_info(self, item):
		item = item.split(' ')
		job, build = item[0], item[1]
		status = item[2].replace('(', '').replace(')', '').lower()
		return build, job, status

	def _is_old_build(self, job, build, status):
		return (job in self.last_displayed
			and self.last_displayed[job] == (build, status))
