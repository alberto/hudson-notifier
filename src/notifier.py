#!/usr/bin/env python
import feedparser
import pynotify
import time

class Notifier():
  BASE_TITLE = 'Hudson Update!'
  TIMEOUT = 1000
  SUCCESS_IMG = 'file:///usr/share/pixmaps/gnome-suse.png'
  UNSTABLE_IMG = 'file:///usr/share/pixmaps/gnome-suse.png'
  FAILURE_IMG = 'file:///usr/share/pixmaps/gnome-suse.png'
  url = 'http://www.newdawnsoftware.com/hudson/view/LWJGL/rssLatest'

  def __init__(self):
	self.last_displayed = dict()
	pynotify.init('Hudson Notify')

  def success(self, job, build):
	n = pynotify.Notification(self.BASE_TITLE,
	'"%s"  %s successfully built :)' % (job, build),
	self.SUCCESS_IMG)
	n.set_urgency(pynotify.URGENCY_LOW)
	n.set_timeout(self.TIMEOUT)
	return n

  def unstable(self, job, build):
	n = pynotify.Notification(self.BASE_TITLE,
		'"%s" %s is unstable :-/' % (job, build),
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

  def main(self):
	while True:
		self.poll()
		time.sleep(60)


  def poll(self):
		print "UPDATING..."	
		url = self.url
		feed = feedparser.parse(url)
		items = [t['title'] for t in feed['entries']]
		for i in items:
			i = i.split(' ')
			job, build, status = (i[0], i[1], i[2])
			
			if job in self.last_displayed and self.last_displayed[job] == (build, status):
				continue
			self.last_displayed[job] = (build, status)
			status = status.replace('(', '').replace(')','')
			if status == 'SUCCESS':
				self.success(job, build).show()
			elif status == 'UNSTABLE':
				self.unstable(job, build).show()
			elif status == 'FAILURE':
				self.failure(job, build).show()
		return True
if __name__ == '__main__':
	Notifier().main()
