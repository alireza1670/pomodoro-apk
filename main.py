from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
import json, os

WORK_DURATION = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60
POMODOROS_BEFORE_LONG_BREAK = 4

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "stats.json")


def init_stats():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)


def save_pomodoro():
    with open(DATA_FILE, "r") as f:
        stats = json.load(f)
    today = datetime.now().strftime("%Y-%m-%d")
    stats[today] = stats.get(today, 0) + 1
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f, indent=2)


class PomodoroUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        init_stats()

        self.mode = "Work"
        self.remaining = WORK_DURATION
        self.pomodoro_count = 0
        self.running = False
        self.event = None

        self.title = Label(text="Pomodoro", font_size=32)
        self.timer_lbl = Label(text=self._fmt(self.remaining), font_size=48)
        self.mode_lbl = Label(text=self.mode, font_size=24)

        btns = BoxLayout(size_hint=(1, None), height=60, spacing=10)
        self.start_btn = Button(text="Start")
        self.pause_btn = Button(text="Pause")
        self.reset_btn = Button(text="Reset")

        self.start_btn.bind(on_press=self.start)
        self.pause_btn.bind(on_press=self.pause)
        self.reset_btn.bind(on_press=self.reset)

        btns.add_widget(self.start_btn)
        btns.add_widget(self.pause_btn)
        btns.add_widget(self.reset_btn)

        self.add_widget(self.title)
        self.add_widget(self.mode_lbl)
        self.add_widget(self.timer_lbl)
        self.add_widget(btns)

    def _fmt(self, sec):
        m = sec // 60
        s = sec % 60
        return f"{m:02d}:{s:02d}"

    def start(self, _):
        if self.running:
            return
        self.running = True
        self.event = Clock.schedule_interval(self.tick, 1)

    def pause(self, _):
        if self.event:
            self.event.cancel()
        self.running = False

    def reset(self, _):
        self.pause(None)
        self.mode = "Work"
        self.remaining = WORK_DURATION
        self.mode_lbl.text = self.mode
        self.timer_lbl.text = self._fmt(self.remaining)

    def tick(self, dt):
        if self.remaining > 0:
            self.remaining -= 1
            self.timer_lbl.text = self._fmt(self.remaining)
            return

        self.pause(None)

        if self.mode == "Work":
            save_pomodoro()
            self.pomodoro_count += 1
            if self.pomodoro_count % POMODOROS_BEFORE_LONG_BREAK == 0:
                self.mode = "Long Break"
                self.remaining = LONG_BREAK
            else:
                self.mode = "Short Break"
                self.remaining = SHORT_BREAK
        else:
            self.mode = "Work"
            self.remaining = WORK_DURATION

        self.mode_lbl.text = self.mode
        self.timer_lbl.text = self._fmt(self.remaining)


class PomodoroApp(App):
    def build(self):
        return PomodoroUI()


if __name__ == "__main__":
    PomodoroApp().run()
