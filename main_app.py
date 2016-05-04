#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from random import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang import Builder
from kivy.factory import Factory
import schedule
import lessons
import popups
# Builder.load_file('./schedule.kv')
# Builder.load_file('./lessons.kv')
# Builder.load_file('./popups.kv')


# class MainWindow(BoxLayout):
#     def __init__(self, **kwargs):
#         super(BoxLayout, self).__init__(orientation='vertical', **kwargs)
#
#         # menu_layout = BoxLayout(size_hint_y=0.8, spacing=3)
#         # buttons = [Button(text="button%d" % (i + 1)) for i in range(6)]
#         # for i in range(6):
#         #     menu_layout.add_widget(buttons[i])
#
#         menu_layout = schedule.LessonBar()
#
#         self.add_widget(menu_layout)
#         lesson_set = [[lessons.data_pair[int(random() * 100) % 2]
#                        for i in range(4)] for j in range(6)]
#         table = schedule.lesson_table_creator(lesson_set=lesson_set)
#         self.add_widget(table)


class MenuApp(App):
    def build(self):
        basic_layout = BoxLayout(orientation='vertical')

        # menu_layout = BoxLayout(size_hint_y=0.08, spacing=2)
        # buttons = [Button(text="button%d" % (i + 1)) for i in range(6)]
        # buttons[0].bind(on_press=self.show_group_popup)
        # for i in range(6):
        #     menu_layout.add_widget(buttons[i])

        menu_layout = Factory.LessonBar()

        basic_layout.add_widget(menu_layout)
        lesson_set = [[lessons.data_pair[int(random() * 100) % 2]
                       for i in range(4)] for j in range(6)]
        table = schedule.lesson_table_creator(lesson_set=lesson_set)
        basic_layout.add_widget(table)
        return basic_layout

    @staticmethod
    def show_group(group):
        print "Group: {}".format(group)


if __name__ == "__main__":
    MenuApp().run()
