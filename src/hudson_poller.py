#!/usr/bin/env python
import feedparser
from rss_parser import RssParser

class HudsonPoller():
	def __init__(self, notifier):
		self.job_results = dict()
		self.notifier = notifier

	def poll(self, urls):
		for url in urls:
			job_results = self.__get_job_results(url)
			for job_result in job_results:
				if self._is_old_build(job_result):
					continue

				self.notifier.notify(job_result).show()
				self.__add_job_result(job_result)
		return self.job_results

	def __get_job_results(self, url):
		feed = feedparser.parse(url)
		items = [t['title'] for t in feed['entries']]
		return [self._get_build_info(item) for item in items]

	def _get_build_info(self, item):
		parser = RssParser()
		return parser.parse(item)

	def _is_old_build(self, job_result):
		if not job_result.job in self.job_results:
			return False

		last_build = self.job_results[job_result.job].build_number
		if job_result.build_number > last_build:
			return False
		return True

	def __add_job_result(self, job_result):
		self.job_results[job_result.job] = job_result
