#!/usr/bin/env python
import feedparser

class HudsonPoller():
	def __init__(self, notifier):
		self.last_displayed = dict()
		self.notifier = notifier

	def poll(self, urls):
		for url in urls:
			feed = feedparser.parse(url)
			items = [t['title'] for t in feed['entries']]
			for item in items:
				build, job, status = self._get_build_info(item)
				if self._is_old_build(job, build, status):
					continue
				self.last_displayed[job] = (build, status)
				self.notifier.notify(job, build, status).show()
		return True

	def _get_build_info(self, item):
		item = item.split(' ')
		job = item[0]
		build = self._parse_build_number(item[1])
		status = self._parse_status(item[2])
		return build, job, status

	def _parse_build_number(self, build):
		build_number = build.replace('#', '')
		return int(build_number)

	def _parse_status(self, status):
		return status.replace('(', '').replace(')', '').lower()

	def _is_old_build(self, job, build, status):
		if not job in self.last_displayed:
			return False
		(last_build, last_status) = self.last_displayed[job]
		if build > last_build:
			return False
		return True
