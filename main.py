import time
import math
import wave
import struct
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def generate_beep_sound(filename="beep.wav", duration=1.0, freq=880.0):
    """Generates a simple 1-second 880Hz beep WAV file if one doesn't exist."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(num_samples):
            val = int(32767.0 * 0.5 * (math.sin(2.0 * math.pi * freq * i / sample_rate)))
            wav_file.writeframes(struct.pack('<h', val))

try:
    generate_beep_sound()
except Exception:
    pass

class ChallengeStopwatch(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # State Variables
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0

        # Load Beep Sound
        self.beep_sound = SoundLoader.load('beep.wav')

        # Main Display Label (Minutes:Seconds.Hundredths)
        self.timer_label = Label(
            text="00:00.00",
            font_size='64sp',
            bold=True,
            color=(0, 1, 0, 1), # Bright green digital display
            size_hint=(1, 0.8)
        )
        self.add_widget(self.timer_label)

        # Bottom Controls Layout
        bottom_panel = BoxLayout(size_hint=(1, 0.2), padding=[15, 10])

        # Bottom Left: "made by syri" label
        left_anchor = AnchorLayout(anchor_x='left', anchor_y='bottom', size_hint=(0.5, 1))
        self.credit_label = Label(
            text="made by syri",
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1), # Light grey tint
            size_hint=(None, None),
            size=(120, 30)
        )
        left_anchor.add_widget(self.credit_label)
        bottom_panel.add_widget(left_anchor)

        # Bottom Right: Smaller Reset Button
        right_anchor = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(0.5, 1))
        self.reset_button = Button(
            text="RESET",
            font_size='14sp',
            bold=True,
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(None, None),
            size=(100, 40) # Smaller, compact button
        )
        self.reset_button.bind(on_press=self.reset_timer)
        right_anchor.add_widget(self.reset_button)
        bottom_panel.add_widget(right_anchor)

        self.add_widget(bottom_panel)

    def on_touch_down(self, touch):
        # Ignore touches intended for the Reset Button
        if self.reset_button.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        # Tap anywhere else on the screen to start/stop
        self.toggle_timer()
        return True

    def toggle_timer(self):
        if not self.running:
            # Play beep ONLY when starting the timer
            if self.beep_sound:
                self.beep_sound.stop()
                self.beep_sound.play()

            # Start timer
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            Clock.schedule_interval(self.update_clock, 1 / 60) # 60 FPS update
        else:
            # Pause timer (no beep played)
            self.running = False
            Clock.unschedule(self.update_clock)

    def update_clock(self, dt):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.render_display()

    def render_display(self):
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        hundredths = int((self.elapsed_time * 100) % 100)

        self.timer_label.text = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    def reset_timer(self, instance):
        if self.running:
            self.running = False
            Clock.unschedule(self.update_clock)
        
        self.elapsed_time = 0.0
        self.render_display()

class StopwatchApp(App):
    def build(self):
        self.title = "Challenge Stopwatch"
        return ChallengeStopwatch()

if __name__ == '__main__':
    StopwatchApp().run()
