#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary popup definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App

# Data, which will form the view of popup, e.g. label, button text
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
data = {
    'group': data_group,
    'teacher': data_teacher,
    'room': data_room
}


class HugePopup(Popup):
    # Popup-form for view schedule for group, teacher or room
    def __init__(self, **kwargs):
        self.label_text = kwargs['label_text']
        self.first_button_label = kwargs['first_button_label']
        self.first_button = kwargs['first_button']
        self.second_button_label = kwargs['second_button_label']
        self.second_button = kwargs['second_button']
        super(Popup, self).__init__(**kwargs)


def simple():
    print "Yes, it works"


def one_more():
    print "Yeah"


class PopupsApp(App):
    def build(self):
        b = Button(on_press=self.show_popup)
        return b

    def show_popup(self, b):
        # p = Builder.template('HugePopup', **data_room)
        # p = popup_create('teacher', simple, one_more)
        p = HugePopup(first_button=simple, second_button=one_more,
                      **data['teacher'])
        p.open()


if __name__ == '__main__':
    PopupsApp().run()
