#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
from poller_factory import PollerFactory
from settings.view import SettingsView
import gobject
import os

class HudsonNotifierUI:
	def __init__(self):
		self.settings_view = SettingsView()
		self.poller = PollerFactory().get()
		self.configure_ui()
		gobject.timeout_add(100, self.poll_first_time)
		gobject.timeout_add(60000, self.poll)
		gtk.main()

	def configure_ui(self):
		self.dir_path = os.path.dirname(__file__)
		MAIN_GLADE = os.path.abspath(self.dir_path + '/main.glade')
		self.gladefile = MAIN_GLADE
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)

		self.statusIcon = self.glade.get_object('tray_icon')
		self.set_success_icon()
		self.liststore = self.glade.get_object('job_results')
		self.treeView = self.glade.get_object('treeview')
		self.connect_events()

	def connect_events(self):
		self.menu = self.glade.get_object('menu')
		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)

		self.jobs = self.glade.get_object('jobs_window')
		self.statusIcon.connect('button-press-event', self.on_tray_icon_button_press_event, self.jobs)

		self.menuItem = self.glade.get_object('settings')
		self.menuItem.connect('activate', self.settings_view.open_prefs, self.statusIcon)

		self.menuItem = self.glade.get_object('quit')
		self.menuItem.connect('activate', self.on_quit_activate, self.statusIcon)

	def poll_first_time(self):
		self.poll()
		return False

	def poll(self):
		urls = self.settings_view.getUrls()
		self.results = self.poller.poll(urls)
		self.update_icon()
		return True

	def update_icon(self):
		failures = filter(lambda x: x.status == 'failure', self.results)
		if len(failures) == 0:
			self.set_success_icon()
		else:
			self.set_fail_icon()

	def set_success_icon(self):
		LOGO = os.path.abspath(self.dir_path + '/../imgs/logo.png')
		self.statusIcon.set_from_file(LOGO)

	def set_fail_icon(self):
		LOGO = os.path.abspath(self.dir_path + '/../imgs/logo_fail.png')
		self.statusIcon.set_from_file(LOGO)

	def on_quit_activate(self, widget, data = None):
		gtk.main_quit()

	def on_tray_icon_button_press_event(self, widget, event, time):
		if (self.__is_button_one_click(event)):
			self.toggle_jobs(time)

	def __is_button_one_click(self, event):
		return event.button == 1

	def popup_menu_cb(self, widget, button, time, data = None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
						3, time, self.statusIcon)

	def toggle_jobs(self, window):
		visibility = window.get_property('visible')
		if visibility == False:
			jobs = self.results
			self.liststore.clear()
			for job in jobs:
				self.liststore.append([job.job, job.build_number, job.status])
			self.treeView.set_model(self.liststore)
			window.show_all()
		else:
			window.hide_all()
		window.set_property('visible', not visibility)

if __name__ == "__main__":
	hn = HudsonNotifierUI()
