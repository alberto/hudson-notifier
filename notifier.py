#!/usr/bin/env python
import feedparser
import pynotify
import time

class Notifier:
  BASE_TITLE = 'Hudson Update!'
  TIMEOUT = 1000

  def __init__(self):
	self.main()

  def success(self, job, build):
	n = pynotify.Notification(self.BASE_TITLE,
	'"%s"  %s successfully built :)' % (job, build),
	'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_urgency(pynotify.URGENCY_LOW)
	n.set_timeout(self.TIMEOUT)
	return n

  def unstable(self, job, build):
	n = pynotify.Notification(self.BASE_TITLE,
		'"%s" %s is unstable :-/' % (job, build),
		'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_timeout(self.TIMEOUT)
	return n

  def failure(self, job, build):
	n = pynotify.Notification(self.BASE_TITLE,
	'"%s" %s failed!' % (job, build),
	'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_urgency(pynotify.URGENCY_CRITICAL)
	n.set_timeout(self.TIMEOUT)
	return n

  def main(self):
	pynotify.init('Hudson Notify')
	last_displayed = dict() 
	while True:
		print "UPDATING..."	
		url = 'http://www.newdawnsoftware.com/hudson/view/LWJGL/rssLatest'
		feed = feedparser.parse(url)
		items = [t['title'] for t in feed['entries']]
		for i in items:
			i = i.split(' ')
			job, build, status = (i[0], i[1], i[2])
			
			if job in last_displayed and last_displayed[job] == (build, status):
				continue
			last_displayed[job] = (build, status)
			status = status.replace('(', '').replace(')','')
			if status == 'SUCCESS':
				self.success(job, build).show()
			elif status == 'UNSTABLE':
				self.unstable(job, build).show()
			elif status == 'FAILURE':
				self.failure(job, build).show()
		time.sleep(20)

if __name__ == '__main__':
	Notifier()
