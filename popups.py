#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary popup definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App


data_group = {
    'title': 'Group schedule',
    'label_text': 'Input the group cypher',
    'first_button': 'Accept',
    'second_button': 'Default'
}
data_teacher = {
    'title': 'Teacher schedule',
    'label_text': 'Input teacher full name',
    'first_button': 'Accept',
    'second_button': 'Default'
}
data_room = {
    'title': 'Room schedule',
    'label_text': 'Input the room number',
    'first_button': 'Accept',
    'second_button': 'All'
}
data = {
    'group': data_group,
    'teacher': data_teacher,
    'room': data_room
}


def popup_create(p_type, first_bind, second_bind):
    popup = Builder.template('HugePopup',
                             first_btn=simple,
                             second_btn=one_more,
                             **data[p_type])
    # popup
    return popup


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
        p = popup_create('teacher', simple, one_more)
        p.open()


if __name__ == '__main__':
    PopupsApp().run()
