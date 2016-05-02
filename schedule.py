#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
import lessons


class ScheduleHolder(BoxLayout):
    def __init__(self, pair_set, **kwargs):
        super(BoxLayout, self).__init__(**kwargs),
        for i in range(len(pair_set)):
            row_box = BoxLayout(orientation='vertical')
            for j in range(len(pair_set[0])):
                paar = lessons.Lesson(**pair_set[i][j])
                button = Button(text=paar.__str__())
                button.bind(texture_size=button.setter('size'))
                row_box.add_widget(button)
            self.add_widget(row_box)


def lesson_holder_creator(pair_set, **kwargs):
    holder = BoxLayout(spacing=3, **kwargs)
    for i in range(len(pair_set)):
        row_box = BoxLayout(orientation='vertical', spacing=3)
        for j in range(len(pair_set[0])):
            lesson = lessons.Lesson(**pair_set[i][j])
            button = Factory.Lesson(text=lesson.__str__())
            row_box.add_widget(button)
        holder.add_widget(row_box)

    return holder


class ScheduleApp(App):
    def build(self):
        hour_box = lesson_holder_creator([[lessons.data_pair[0] for i in range(4)]
                                         for j in range(5)])
        return hour_box


if __name__ == '__main__':
    ScheduleApp().run()
