#!/usr/bin/env python
import feedparser
from rss_parser import RssParser

class HudsonPoller():
	def __init__(self, notifier):
		self.last_displayed = dict()
		self.notifier = notifier

	def poll(self, urls):
		for url in urls:
			feed = feedparser.parse(url)
			items = [t['title'] for t in feed['entries']]
			for item in items:
				job_result = self._get_build_info(item)
				if self._is_old_build(job_result):
					continue
				self.__add_job_result(job_result)

				self.notifier.notify(job_result).show()
		return True

	def _get_build_info(self, item):
		parser = RssParser()
		return parser.parse(item)

	def _is_old_build(self, job_result):
		if not job_result.job in self.last_displayed:
			return False
		last_build = self.last_displayed[job_result.job][0]
		if job_result.build_number > last_build:
			return False
		return True

	def __add_job_result(self, job_result):
		self.last_displayed[job_result.job] = (job_result.build_number, job_result.status)
