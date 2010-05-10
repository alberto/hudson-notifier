class JobResult():
	def __init__(self, job, build_number, status):
		self.job = job
		self.build_number = build_number
		self.status = status

	def __repr__(self):
		return "job: %s, build number: %s, status: %s" % (self.job, self.build_number, self.status)
