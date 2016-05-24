#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary popup definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from database import teacher_list
from kivy.app import App


# Data which will form the view of popup, e.g. label, button text
# Division may be useful for translation
data_group = {
    'title': 'Group schedule',
    'btn_text': 'Choose group cypher'
}
data_teacher = {
    'title': 'Teacher schedule',
    'btn_text': 'Choose teacher'
}
data_room = {
    'title': 'Room schedule',
    'btn_text': 'Choose room number'
}
popup_data = {
    'group': data_group,
    'teacher': data_teacher,
    'room': data_room
}


class ChoicePopup(Popup):
    """
    Popup form for view schedule for group, teacher or room
    """
    btn_text = StringProperty()
    choices = ListProperty()
    choice_btn = ObjectProperty(None)
    on_release = ObjectProperty()

    def __init__(self, on_release, **kwargs):
        self.on_release = on_release
        super(ChoicePopup, self).__init__(**kwargs)
        drop_down = DropDown()

        for choice in self.choices:
            button = Button(
                text=str(choice) if isinstance(choice, int) else choice,
                size_hint_y=None,
                height=35
            )
            button.bind(on_release=lambda btn: drop_down.select(btn.text))
            drop_down.add_widget(button)
        self.choice_btn.bind(on_release=drop_down.open)
        drop_down.bind(
            on_select=lambda instance, x: setattr(self.choice_btn, 'text', x)
        )


class LoginPopup(Popup):
    """
    Popup form for logging in
    """
    login_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, accept, **kwargs):
        self.accept = accept
        super(Popup, self).__init__(**kwargs)


class LessonPopup(Popup):
    """
    Popup form for editing the lesson object
    """

    def __init__(self, **kwargs):
        super(LessonPopup, self).__init__(**kwargs)


class PopupsApp(App):
    def build(self):
        b = Button(on_press=self.show_popup)
        bl = Button(on_press=self.show_login_popup)
        box = BoxLayout()
        box.add_widget(b)
        box.add_widget(bl)
        return box

    def show_popup(self, b):
        # LessonPopup().open()
        ChoicePopup(
            choices=teacher_list,
            on_release=print_function,
            **popup_data['teacher']
        ).open()

    def show_login_popup(self, b):
        LoginPopup(accept=self.login_show).open()

    def login_show(self, login, password):
        print "Login: %s, Pass: %s" % (login, password)


if __name__ == '__main__':
    PopupsApp().run()
