import os
import math
import struct
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

Window.clearcolor = (0, 0, 0, 1)

def create_wav_file(filename, duration, frequency=800.0):
    """Generates and writes a valid PCM WAV sound file to disk."""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    
    audio_data = bytearray()
    for i in range(num_samples):
        sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
        audio_data.extend(struct.pack('<h', sample))
        
    header = bytearray(b'RIFF')
    header.extend(struct.pack('<I', 36 + len(audio_data)))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    header.extend(b'data')
    header.extend(struct.pack('<I', len(audio_data)))
    
    filepath = os.path.join(App.get_running_app().user_data_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(header + audio_data)
    return filepath

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_elapsed = 0.0
        self.is_running = False

        # Load sound files
        try:
            start_path = create_wav_file('start_beep.wav', 0.99, frequency=880.0)
            stop_path = create_wav_file('stop_beep.wav', 0.15, frequency=660.0)  # Shortened to 0.15s
            self.start_sound = SoundLoader.load(start_path)
            self.stop_sound = SoundLoader.load(stop_path)
        except Exception:
            self.start_sound = None
            self.stop_sound = None

        # Timer Display (Centered)
        self.timer_label = Label(
            text="00:00.00",
            font_size='80sp',
            bold=True,
            color=(0, 1, 0, 1),
            size_hint=(1, None),
            height=120,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        # Made by syri Label (Centered right under the timer)
        self.syri_label = Label(
            text="Made by syri",
            font_size='22sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.42}
        )

        self.add_widget(self.timer_label)
        self.add_widget(self.syri_label)

    def on_touch_down(self, touch):
        """Triggers when tapping anywhere on the screen."""
        if self.is_running:
            # STOP: Pause timer and play short 0.15s beep
            Clock.unschedule(self.update_timer)
            self.is_running = False
            if self.stop_sound:
                self.stop_sound.play()
        else:
            if self.time_elapsed > 0.0:
                # RESET if stopped with time on clock
                self.time_elapsed = 0.0
                self.timer_label.text = "00:00.00"
            else:
                # START: Play 0.99s beep and start timer
                if self.start_sound:
                    self.start_sound.play()
                Clock.schedule_interval(self.update_timer, 0.05)
                self.is_running = True
        return True

    def update_timer(self, dt):
        self.time_elapsed += dt
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        centiseconds = int((self.time_elapsed * 100) % 100)
        self.timer_label.text = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

class TimerApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    TimerApp().run()
