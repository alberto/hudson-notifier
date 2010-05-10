#!/usr/bin/env python
import pynotify
import os

class LibNotifyNotifier():
	BASE_TITLE = 'Hudson Update'
	TIMEOUT = 1000
	dir_path = os.path.dirname(__file__)
	SUCCESS_IMG = os.path.abspath(dir_path + '/../imgs/success.png')
	UNSTABLE_IMG = os.path.abspath(dir_path + '/../imgs/unstable.png')
	FAILURE_IMG = os.path.abspath(dir_path + '/../imgs/failure.png')

	statuses = {
		'success' : [ '"%s" #%s successfully built.', SUCCESS_IMG, pynotify.URGENCY_LOW],
		'unstable' : [ '"%s" #%s is unstable.', UNSTABLE_IMG, pynotify.URGENCY_NORMAL],
		'failure' : [ '"%s" #%s failed!', FAILURE_IMG, pynotify.URGENCY_CRITICAL]
	}

	def __init__(self):
		pynotify.init('Hudson Notifier')

	def notify(self, job_result):
		status_values = self.statuses[job_result.status]
		n = pynotify.Notification(
			self.BASE_TITLE,
			status_values[0] % (job_result.job, job_result.build_number),
			status_values[1])
		n.set_urgency(status_values[2])
		n.set_timeout(self.TIMEOUT)
		return n
