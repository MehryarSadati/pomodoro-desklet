import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Glib, Notify
import time

class PomodoroDesklet(Gtk.Window):
    def __init___(self):
        super().__init__(title="Pomodoro Timer")

        Notify.init("Pomodro Desklet")

        #setting the default mode
        self.work_duration = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 20 * 60
        self.reps_before_long_break = 4
        self.current_rep = 0

        self.remaining_time = 0
        self.is_running = False
        self.is_work_time = True

        self.setup_ui()

        self.set_keep_below(True)
        self.set_decorated(False)
        self.stick()

    def setup_ui(self):
        pass

    def update_time_display(self):
        pass

    def on_start_clicked(self, widget):
        pass

    def on_reset_clicked(self, widget):
        pass

    def start_timer(self):
        pass

    def pause_timer(self):
        pass

    def reset_timer(self):
        pass

    def on_timer_tick(self):
        pass

    def timer_completed(self):
        pass

    