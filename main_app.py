#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from random import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionButton
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang import Builder
import schedule
import lessons
import popups
Builder.load_file('./schedule.kv')
# Builder.load_file('./lessons.py')
Builder.load_file('./popups.kv')


'''
class PopupsApp(App):
    def build(self):
        b = Button(on_press=self.show_popup)
        return b

    def show_popup(self, b):
        p = Builder.template('HugePopup', **data_room)
        p.open()

        self.hello.bind(on_press=self.auth)
'''


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(orientation='vertical', **kwargs)
        menu_layout = BoxLayout(size_hint_y=0.8, spacing=3)
        buttons = [ActionButton(text="button%d" % (i + 1)) for i in range(6)]
        for i in range(6):
            menu_layout.add_widget(buttons[i])
        self.add_widget(menu_layout)
        lesson_set = [[lessons.data_pair[int(random() * 100) % 2]
                       for i in range(4)] for j in range(5)]
        table = schedule.lesson_holder_creator(pair_set=lesson_set)
        tabs = TabbedPanel(do_default_tab=False)
        for i in range(3):
            tab = TabbedPanelItem(content=table, text='tab № {}'.format(i + 1))
            tabs.add_widget(tab)
        self.add_widget(tabs)


class MenuApp(App):
    def build(self):
        menu_layout = BoxLayout(size_hint_y=0.08, spacing=3)
        basic_layout = BoxLayout(orientation='vertical')
        buttons = [Button(text="button%d" % (i + 1)) for i in range(6)]
        buttons[0].bind(on_press=self.show_group_popup)
        for i in range(6):
            menu_layout.add_widget(buttons[i])
        basic_layout.add_widget(menu_layout)
        lesson_set = [[lessons.data_pair[int(random() * 100) % 2]
                       for i in range(4)] for j in range(5)]
        table = schedule.lesson_holder_creator(pair_set=lesson_set)
        tabs = TabbedPanel(do_default_tab=False)
        for i in range(3):
            tab = TabbedPanelItem(content=table, text='tab № {}'.format(i + 1))
            tabs.add_widget(tab)
        basic_layout.add_widget(tabs)

        # basic_layout = MainWindow()
        return basic_layout

    @staticmethod
    def show_group_popup(b):
        p = Builder.template('HugePopup', **popups.data_group)
        p.open()

    @staticmethod
    def show_teacher_popup(b):
        p = Builder.template('HugePopup', **popups.data_teacher)
        p.open()

    @staticmethod
    def show_room_popup(b):
        p = Builder.template('HugePopup', **popups.data_room)
        p.open()


if __name__ == "__main__":
    MenuApp().run()
