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
    'title': _('Group schedule'),
    'btn_text': _('Choose group cypher')
}
data_teacher = {
    'title': _('Teacher schedule'),
    'btn_text': _('Choose teacher')
}
data_room = {
    'title': _('Room schedule'),
    'btn_text': _('Choose room number')
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
    choice_input = ObjectProperty(None)
    on_release = ObjectProperty(None)
    dropdown = ObjectProperty(None)

    def __init__(self, on_release, **kwargs):
        self.on_release = on_release
        super(ChoicePopup, self).__init__(**kwargs)
        self.dropdown = DropDown()
        self.choice_input.bind(text=self.make_dropdown, focus=self.on_focus)
        self.dropdown.bind(
            on_select=lambda instance, x: setattr(self.choice_input, 'text', x)
        )

    def make_dropdown(self, *args):
        self.dropdown.clear_widgets()
        for choice in self.choices:
            if self.choice_input.text in choice or self.choice_input.text == '':
                button = Button(
                    text=choice,
                    size_hint_y=None,
                    height=35
                )
                button.bind(
                    on_release=lambda btn: self.dropdown.select(btn.text)
                )
                self.dropdown.add_widget(button)
            else:
                pass
        self.dropdown.open(self.choice_input)

    @staticmethod
    def on_focus(instance, value):
        if value:
            instance.text = ''


class LoginPopup(Popup):
    """
    Popup form for logging in
    """
    login_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, accept, **kwargs):
        self.accept = accept
        super(Popup, self).__init__(**kwargs)


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
