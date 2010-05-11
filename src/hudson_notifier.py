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
		self.__configure_ui()
		gobject.timeout_add(100, self.__poll_first_time)
		gobject.timeout_add(60000, self.__poll)
		gtk.main()

	def on_quit_activate(self, widget, data = None):
		gtk.main_quit()

	def on_tray_icon_button_press_event(self, widget, event, time):
		if (self.__is_button_one_click(event)):
			self.__toggle_jobs(time)

	def popup_menu_cb(self, widget, button, time, data = None):
		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
						3, time, self.statusIcon)

	def __configure_ui(self):
		self.dir_path = os.path.dirname(__file__)
		MAIN_GLADE = os.path.abspath(self.dir_path + '/main.glade')
		self.gladefile = MAIN_GLADE
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		path_to_fail_icon = os.path.abspath(self.dir_path + '/../imgs/icon_failure.png')
		path_to_success_icon = os.path.abspath(self.dir_path + '/../imgs/icon_success.png')
		self.fail_icon = gtk.gdk.pixbuf_new_from_file(path_to_fail_icon)
		self.success_icon = gtk.gdk.pixbuf_new_from_file(path_to_success_icon)
		self.statusIcon = self.glade.get_object('tray_icon')
		self.__set_success_icon()
		self.liststore = self.glade.get_object('job_results')
		self.treeView = self.glade.get_object('treeview')
		self.__connect_events()
		width, height = self.jobs.get_position()
		self.jobs.move(width, height + 20)

	def __connect_events(self):
		self.menu = self.glade.get_object('menu')
		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)

		self.jobs = self.glade.get_object('jobs_window')
		self.statusIcon.connect('button-press-event', self.on_tray_icon_button_press_event, self.jobs)

		self.menuItem = self.glade.get_object('settings')
		self.menuItem.connect('activate', self.settings_view.open_prefs, self.statusIcon)

		self.menuItem = self.glade.get_object('quit')
		self.menuItem.connect('activate', self.on_quit_activate, self.statusIcon)

	def __poll_first_time(self):
		self.__poll()
		return False

	def __poll(self):
		urls = self.settings_view.getUrls()
		self.results = self.poller.poll(urls)
		self.__update_icon()
		return True

	def __update_icon(self):
		failures = filter(lambda x: x.status == 'failure', self.results.itervalues())
		if len(failures) == 0:
			self.__set_success_icon()
		else:
			self.__set_fail_icon()

	def __set_success_icon(self):
		LOGO = os.path.abspath(self.dir_path + '/../imgs/logo.png')
		self.statusIcon.set_from_file(LOGO)

	def __set_fail_icon(self):
		LOGO = os.path.abspath(self.dir_path + '/../imgs/logo_fail.png')
		self.statusIcon.set_from_file(LOGO)

	def __is_button_one_click(self, event):
		return event.button == 1

	def __toggle_jobs(self, window):
		is_visible = window.get_property('visible')
		if is_visible == False:
			jobs = self.results.itervalues()
			self.liststore.clear()
			for job in jobs:
				text = "%s #%s" % (job.job, job.build_number)
				image = self.__get_small_icon(job.status)
				self.liststore.append([image, text])
			self.treeView.set_model(self.liststore)

			width, height = window.get_position()
			window.move(width, height + 20)

			window.show_all()
		else:
			window.hide_all()
		window.set_property('visible', not is_visible)

	def __get_small_icon(self, status):
		if status == "success":
			return self.success_icon
		else:
			return self.fail_icon

if __name__ == "__main__":
	hn = HudsonNotifierUI()
