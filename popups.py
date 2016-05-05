#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary popup definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App

# Data which will form the view of popup, e.g. label, button text
# Division may be useful for translation
data_group = {
    'title': 'Group schedule',
    'label_text': 'Input the group cypher',
    'first_button_label': 'Accept',
    'second_button_label': 'Default'
}
data_teacher = {
    'title': 'Teacher schedule',
    'label_text': 'Input teacher full name',
    'first_button_label': 'Accept',
    'second_button_label': 'Default'
}
data_room = {
    'title': 'Room schedule',
    'label_text': 'Input the room number',
    'first_button_label': 'Accept',
    'second_button_label': 'All'
}
popup_data = {
    'group': data_group,
    'teacher': data_teacher,
    'room': data_room
}


class HugePopup(Popup):
    # Popup-form for view schedule for group, teacher or room
    label_text = StringProperty()
    text_input = ObjectProperty(None)
    first_button_label = StringProperty()
    second_button_label = StringProperty()

    def __init__(self, **kwargs):
        self.first_button = kwargs['first_button']
        self.second_button = kwargs['second_button']
        super(Popup, self).__init__(**kwargs)


class LoginPopup(Popup):
    # Popup-form for login
    login_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, accept, **kwargs):
        self.accept = accept
        super(Popup, self).__init__(**kwargs)


def simple(b):
    print "Yes, it works: {}".format(b)


def one_more(b):
    print "Yeah: {}".format(b)


class PopupsApp(App):
    def build(self):
        b = Button(on_press=self.show_popup)
        bl = Button(on_press=self.show_login_popup)
        box = BoxLayout()
        box.add_widget(b)
        box.add_widget(bl)
        return box

    def show_popup(self, b):
        p = HugePopup(first_button=simple, second_button=one_more,
                      **popup_data['teacher'])
        p.open()

    def show_login_popup(self, b):
        p = LoginPopup(accept=self.login_show)
        p.open()

    def login_show(self, login, password):
        print "Login: %s, Pass: %s" % (login, password)


if __name__ == '__main__':
    PopupsApp().run()
