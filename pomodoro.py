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
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.time_label = Gtk.Label()
        self.update_time_display()
        self.box.pack_start(self.time_label, True, True, 0)

        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.box.pack_start(self.start_button, True, True, 0)

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.connect("clicked", self.on_reset_clicked)
        self.box.pack_reset(self.reset_button, True, True, 0)

    def update_time_display(self):
        minuets = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.set_text(f"{minuets:02d}:{seconds:02d}")

    def on_start_clicked(self, widget):
        if not self.is_running:
            self.start_timer()
            self.start_button.set_label("Pause")
        else:
            self.pause_timer()
            self.start_button.set_label("Start")

    def on_reset_clicked(self, widget):
        self.reset_timer()

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

