#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, GLib, Notify
import time
from pygame import mixer

mixer.init()
SOUND = mixer.Sound("beep.wav")

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent, config):
        super().__init__(title="Settings", transient_for=parent, flags=0)
        self.config = config
        
        self.set_default_size(300, 200)
        self.set_modal(True)
        self.set_border_width(10)

        box = self.get_content_area()

        # grid = Gtk.Grid(column_spacing=12, row_spacing=12, margin=12)
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)        

        #work duration
        work_label = Gtk.Label(label="Work Duration (minuets):", xalign=0)
        self.work_spin = Gtk.SpinButton.new_with_range(1, 60, 1)
        self.work_spin.set_value(self.config['work_duration'] / 60)
        grid.attach(work_label, 0, 0, 1, 1)
        grid.attach(self.work_spin, 1, 0, 1, 1)
        
        #short break button
        short_break_label = Gtk.Label(label="Short Break (minuets):", xalign=0)
        self.short_break_spin = Gtk.SpinButton.new_with_range(1, 60, 1)
        self.short_break_spin.set_value(self.config['short_break'] / 60)
        grid.attach(short_break_label, 0, 1, 1, 1)
        grid.attach(self.short_break_spin, 1, 1, 1, 1)

        #long break button
        long_break_label = Gtk.Label(label="Long Break (minuets):", xalign=0)
        self.long_break_spin = Gtk.SpinButton.new_with_range(1, 60, 1)
        self.long_break_spin.set_value(self.config['long_break'] / 60)
        grid.attach(long_break_label, 0, 2, 1, 1)
        grid.attach(self.long_break_spin, 1, 2, 1, 1)

        # content_area().add(grid)
        box.add(grid)

        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        self.show_all()

    def get_updated_config(self):
        return {
            'work_duration' : self.work_spin.get_value() * 60, 
            'short_break' : self.short_break_spin.get_value() * 60,
            'long_break' : self.long_break_spin.get_value() * 60
        }

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

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.box.pack_start(self.start_button, True, True, 0)

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.connect("clicked", self.on_reset_clicked)
        self.box.pack_start(self.reset_button, True, True, 0)

        self.setting_button = Gtk.Button.new_from_icon_name("preferences-system-symbolic", Gtk.IconSize.BUTTON)
        self.setting_button.connect("clicked", self.on_settings_clicked)
        button_box.pack_start(self.setting_button, True, True, 0)

        self.box.pack_start(button_box, True, True, 0)

    def update_time_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.set_text(f"{int(minutes):02d}:{int(seconds):02d}")

    def on_start_clicked(self, widget):
        if not self.is_running:
            self.start_timer()
            self.start_button.set_label("Pause")
        else:
            self.pause_timer()
            self.start_button.set_label("Start")

    def on_reset_clicked(self, widget):
        self.reset_timer()

    def on_settings_clicked(self, widget):
        dialog = SettingsDialog(self, self.get_current_config())
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.apply_new_settings(dialog.get_updated_config())

        dialog.destroy()

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

    def get_current_config(self):
        return {
            'work_duration': self.work_duration,
            'short_break': self.short_break, 
            'long_break': self.long_break
        }
    
    def apply_new_settings(self, new_config):
        self.work_duration = new_config['work_duration']
        self.short_break = new_config['short_break']
        self.long_break = new_config['long_break']

        if not self.is_running:
            self.reset_timer()


if __name__ == "__main__":
    window = PomodoroDesklet()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
