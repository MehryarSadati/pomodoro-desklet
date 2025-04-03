#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, GLib, Notify
import time
from pygame import mixer

mixer.init()
SOUND = mixer.Sound("beep.wav")

class Setting(Gtk.Dialog):
    def __init__(self, parent, config):
        super.__init__(title="Setting", transient_for=parent, flag=0)
        self.config = config

        self.create_ui()

    def create_ui(self):
        pass

class PomodoroDesklet(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pomodoro Timer")

        Notify.init("Pomodoro Desklet")

        # setting the default mode
        self.work_duration = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 20 * 60
        self.reps_before_long_break = 4

        self.current_rep = 0
        self.is_running = False
        self.remaining_time = self.work_duration
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
        self.box.pack_start(self.reset_button, True, True, 0)

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
        if not self.is_running:
            self.is_running = True
            self.timeout_id = GLib.timeout_add_seconds(1, self.on_timer_tick)
            SOUND.play()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            GLib.source_remove(self.timeout_id)
            SOUND.play()

    def reset_timer(self):
        self.pause_timer()
        SOUND.play()
        if self.is_work_time:
            self.remaining_time = self.work_duration
        else:
            if self.current_rep % self.reps_before_long_break == 0:
                self.remaining_time = self.long_break
            else:
                self.remaining_time = self.short_break

        self.update_time_display()
        self.start_button.set_label("Start")

    def on_timer_tick(self):
        if self.is_running:
            self.remaining_time -= 1
            self.update_time_display()

            if self.remaining_time <= 0:
                self.timer_completed()
                return False

        return True

    def timer_completed(self):
        self.is_running = False

        notification = Notify.Notification.new(
            "Pomodoro",
            "Work time is over!" if self.is_work_time else "Break time is over!",
            "dialog-information",
        )
        notification.show()

        self.is_work_time = not self.is_work_time
        if not self.is_work_time:
            self.current_rep += 1

        self.reset_timer()
        SOUND.play()


if __name__ == "__main__":
    window = PomodoroDesklet()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
