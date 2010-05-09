from job_result import JobResult

class RssParser():
	def parse(self, rss_item):
		hash = rss_item.rfind("#")
		left_paren = rss_item.rfind("(")
		right_paren = rss_item.rfind(")")
		job = rss_item[0:hash]
		build = rss_item[hash + 1:left_paren]
		status = rss_item[left_paren + 1:right_paren].lower()
		return JobResult(job, build, status)

	def _parse_build_number(self, build):
		build_number = build.replace('#', '')
		return int(build_number)

	def _parse_status(self, status):
		return status.replace('(', '').replace(')', '').lower()
