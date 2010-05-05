from hudson_poller import HudsonPoller
from libnotify_notifier import LibNotifyNotifier

class PollerFactory():
	def get(self):
		return HudsonPoller(LibNotifyNotifier())
