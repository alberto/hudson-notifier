#!/usr/bin/env python
import feedparser
import pynotify
import time

BASE_TITLE = 'Hudson Update!'
TIMEOUT = 3000

def success(job, build):
	n = pynotify.Notification(BASE_TITLE,
	'"%s"  %s successfully built :)' % (job, build),
	'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_urgency(pynotify.URGENCY_LOW)
	n.set_timeout(TIMEOUT)
	return n

def unstable(job, build):
	n = pynotify.Notification(BASE_TITLE,
		'"%s" %s is unstable :-/' % (job, build),
		'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_timeout(TIMEOUT)
	return n

def failure(job, build):
	n = pynotify.Notification(BASE_TITLE,
	'"%s" %s failed!' % (job, build),
	'file:///usr/share/pixmaps/gnome-suse.png')
	n.set_urgency(pynotify.URGENCY_CRITICAL)
	n.set_timeout(TIMEOUT)
	return n

def main():
	pynotify.init('Hudson Notify')
	last_displayed = {}
	while True:
		url = 'http://www.newdawnsoftware.com/hudson/view/LWJGL/rssLatest'
		feed = feedparser.parse(url)
		items = [t['title'] for t in feed['entries']]
		for i in items:
			i = i.split(' ')
			print i
			job, build, status = (i[0], i[1], i[2])
			if last_displayed.get(job) == (build, status):
				continue
			last_displayed[job] = (build, status)
			status = status.replace('(', '').replace(')','')
			if status == 'SUCCESS':
				success(job, build).show()
			elif status == 'UNSTABLE':
				unstable(job, build).show()
			elif status == 'FAILURE':
				failure(job, build).show()

		last_displayed = items
		time.sleep(60)

if __name__ == '__main__':
	main()
