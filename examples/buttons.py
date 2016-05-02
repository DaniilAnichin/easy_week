from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.app import App


def callback(instance):
    print('The button <%s> is being pressed' % instance.text)


class ButtonApp(App):
    def build(self):
        box = BoxLayout()
        # btn1 = ToggleButton(text='Male', group='sex', )
        # btn2 = ToggleButton(text='Female', group='sex', state='down')
        # btn3 = ToggleButton(text='Mixed', group='sex')
        # box.add_widget(btn1)
        # box.add_widget(btn2)
        # box.add_widget(btn3)
        btn = Button(text='Quit?', font_size=14)
        btn.bind(on_press=callback)
        box.add_widget(btn)
        return box

ButtonApp().run()
