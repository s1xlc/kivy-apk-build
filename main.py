import math
import struct
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Line

Window.clearcolor = (0, 0, 0, 1)

def generate_beep_sound():
    """Generates a 0.5-second sine wave beep sound dynamically."""
    sample_rate = 22050
    duration = 0.5  # 0.5 seconds
    frequency = 800.0  # 800 Hz pitch
    num_samples = int(sample_rate * duration)
    
    audio_data = bytearray()
    for i in range(num_samples):
        # Generate 16-bit PCM mono audio sample
        sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
        audio_data.extend(struct.pack('<h', sample))
        
    # Standard WAV Header (44 bytes)
    header = bytearray(b'RIFF')
    header.extend(struct.pack('<I', 36 + len(audio_data)))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    header.extend(b'data')
    header.extend(struct.pack('<I', len(audio_data)))
    
    wav_bytes = bytes(header + audio_data)
    sound = SoundLoader.load_data(wav_bytes, ext='wav')
    return sound

class BorderedButton(Button):
    """Button widget with a custom border frame outline."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.after:
            Color(1, 1, 1, 0.8)  # White border color
            self.border_line = Line(width=1.5)
        self.bind(pos=self._update_border, size=self._update_border)

    def _update_border(self, *args):
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)

class TimerApp(App):
    def build(self):
        self.time_elapsed = 0.0
        self.is_running = False
        
        # Load the 0.5s beep sound
        try:
            self.beep_sound = generate_beep_sound()
        except Exception:
            self.beep_sound = None

        # Main Layout
        main_layout = BoxLayout(orientation='vertical')

        # Center area for the main timer display
        timer_container = AnchorLayout(anchor_x='center', anchor_y='center')
        
        self.timer_label = Button(
            text="00:00.00",
            font_size='90sp',
            bold=True,
            color=(0, 1, 0, 1),
            background_color=(0, 0, 0, 0),
            background_normal='',
            size_hint=(None, None),
            size=(Window.width, 250)
        )
        self.timer_label.bind(on_press=self.handle_timer_tap)
        timer_container.add_widget(self.timer_label)
        main_layout.add_widget(timer_container)

        # Bottom Bar for "Made by syri" and "RESET"
        bottom_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=70,
            padding=[25, 10, 25, 20]
        )

        # Made by syri Label (Bold & White Color)
        syri_label = Label(
            text="Made by syri",
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='left',
            valign='center'
        )
        syri_label.bind(size=syri_label.setter('text_size'))

        # RESET Button with border frame outline
        reset_btn = BorderedButton(
            text="RESET",
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            background_color=(0, 0, 0, 0),
            background_normal='',
            size_hint=(None, None),
            size=(110, 45)
        )
        reset_btn.bind(on_press=self.reset_timer)

        bottom_bar.add_widget(syri_label)
        bottom_bar.add_widget(reset_btn)

        main_layout.add_widget(bottom_bar)

        return main_layout

    def handle_timer_tap(self, instance):
        if self.is_running:
            # Tap to STOP: Pause timer and play 0.5s beep
            Clock.unschedule(self.update_timer)
            self.is_running = False
            if self.beep_sound:
                self.beep_sound.play()
        else:
            # Tap again while stopped: RESET or START if already 0
            if self.time_elapsed > 0.0:
                self.time_elapsed = 0.0
                self.timer_label.text = "00:00.00"
            else:
                Clock.schedule_interval(self.update_timer, 0.05)
                self.is_running = True

    def update_timer(self, dt):
        self.time_elapsed += dt
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        centiseconds = int((self.time_elapsed * 100) % 100)
        self.timer_label.text = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

    def reset_timer(self, instance):
        if self.is_running:
            Clock.unschedule(self.update_timer)
            self.is_running = False
        self.time_elapsed = 0.0
        self.timer_label.text = "00:00.00"

if __name__ == '__main__':
    TimerApp().run()
