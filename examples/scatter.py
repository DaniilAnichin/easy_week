from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.app import App


class MyScatter(Scatter):
    pass


class ScatterApp(App):
    def build(self):
        s = MyScatter(size=(400, 400), size_hint=(None, None))
        label = Label(text="Hello!", font_size=150)
        s.add_widget(label)
        s.top = 500
        return s

ScatterApp().run()
