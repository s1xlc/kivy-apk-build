from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0, 0, 0, 1)

class TimerApp(App):
    def build(self):
        self.time_elapsed = 0.0
        self.is_running = False

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
            size=(Window.width, 200)
        )
        self.timer_label.bind(on_press=self.toggle_timer)
        timer_container.add_widget(self.timer_label)
        main_layout.add_widget(timer_container)

        # Bottom Bar for "Made by syri" and "RESET"
        bottom_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            padding=[20, 10, 20, 15]
        )

        # Made by syri Label (Bold, White & Bright)
        syri_label = Label(
            text="Made by syri",
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='left',
            valign='center'
        )
        syri_label.bind(size=syri_label.setter('text_size'))

        # RESET Button (Bold, White & Bright)
        reset_btn = Button(
            text="RESET",
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            background_color=(0, 0, 0, 0),
            background_normal='',
            size_hint_x=None,
            width=100
        )
        reset_btn.bind(on_press=self.reset_timer)

        bottom_bar.add_widget(syri_label)
        bottom_bar.add_widget(reset_btn)

        main_layout.add_widget(bottom_bar)

        return main_layout

    def toggle_timer(self, instance):
        if self.is_running:
            Clock.unschedule(self.update_timer)
            self.is_running = False
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
