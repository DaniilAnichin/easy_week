from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder

# You could also put the following in your kv file...
kv = '''
<DragLabel>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 1000
    drag_distance: 0
    canvas.before:
        Color:
            rgba: .5, .5, .5, 1.0
        Rectangle:
            pos: self.pos
            size: self.size

<DragButton>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 1000
    drag_distance: 0
    disabled: False
    canvas.before:
        Color:
            rgba: .5, .5, .5, 1.0
        Rectangle:
            pos: self.pos
            size: self.size


FloatLayout:
    # Define the root widget
    DragButton:
        size_hint: 0.5, 0.5
        pos: 0, 0
        text: 'Drag me'
    DragButton:
        size_hint: 0.5, 0.5
        pos: root.width / 2, 0
        text: 'Drag 2'
    DragButton:
        size_hint: 0.5, 0.5
        pos: 0, root.height / 2
        text: 'Drag 3'
'''


class DragLabel(DragBehavior, Label):
    pass


class DragButton(DragBehavior, Button):
    pass


class DragApp(App):
    def build(self):
        return Builder.load_string(kv)

DragApp().run()
