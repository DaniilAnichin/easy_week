#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Main window for easy week, includes Action bar and logging
"""
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.actionbar import ActionBar
from kivy.properties import ListProperty, OptionProperty, ObjectProperty, \
    StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from schedule import LessonDay, LessonWeek, LessonTable
from lessons import data_lesson, Lesson, lesson_click
from popups import HugePopup, LoginPopup, popup_data
from database import get_lesson_set


class NoOverScroll(ScrollEffect):
    pass


class MainWindow(BoxLayout):
    lesson_set = ListProperty()
    log_label = ObjectProperty(None)
    table_type = OptionProperty('groups', options=['groups', 'group',
                                                   'teachers', 'teacher',
                                                   'rooms', 'room'])
    content = StringProperty()
    scroll_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.no_resize = True
        self.scroll_layout.effect_cls = NoOverScroll
        self.log_label.text = 'loading database...(wait a bit, pls)'
        Clock.schedule_once(lambda dt: self.load_database(), 1)

    def load_database(self):
        self.lesson_set = get_lesson_set()
        self.log_label.text = 'Database loaded successfully'
        self.set_table(self.table_type)

    def set_table(self, table_type, content=None):
        self.log_label.text = 'Preparing data'
        try:
            self.table_type = table_type
        except ValueError:
            return -1

        self.clear_table()

        if self.table_type.endswith('s'):
            self.no_resize = True
            lesson_table = LessonTable(lesson_set=self.lesson_set,
                                       size_hint=(None, None),
                                       pos_hint={'top': 1, 'left': 1})
            lesson_table.bind(minimum_height=lesson_table.setter('height'))
            lesson_table.bind(minimum_width=lesson_table.setter('width'))
        else:
            self.no_resize = False
            for day in self.lesson_set:
                for lesson in day:
                    lesson.view_type = self.table_type
            lesson_table = LessonWeek(day_set=[LessonDay(lesson_set=day)
                                               for day in self.lesson_set])

        self.log_label.text = 'Showing %s table' % table_type
        self.log_label.text += ' for %s' % content if content is not None else ''
        self.scroll_layout.add_widget(lesson_table)

    def clear_table(self):
        if len(self.scroll_layout.children) is 0:
            return 0

        if isinstance(self.scroll_layout.children[0], BoxLayout):
            # if LessonWeek was used:
            # print type(self.scroll_layout.children)
            for child in self.scroll_layout.children[0].children:
                child.clear_widgets()
        else:
            # if the LessonTable:
            self.scroll_layout.children[0].clear_widgets()

        self.scroll_layout.clear_widgets()

    def login(self, login, password):
        # if users['login'].password == password: (from db)
        # self.user = ...
        self.log_label.text = 'You have logged in as %s' % login
        # else:
        #     self.log_label.text = 'Incorrect password, try again'

    # Helpful functions
    def logout(self):
        # self.user = ...
        self.log_label.text = 'You have logged out'

    def show_group_popup(self):
        p = HugePopup(first_button=partial(self.set_table, 'group'),
                      second_button=partial(self.set_table, 'groups'),
                      **popup_data['group'])
        p.open()

    def show_teacher_popup(self):
        p = HugePopup(first_button=partial(self.set_table, 'teacher'),
                      second_button=partial(self.set_table, 'teachers'),
                      **popup_data['teacher'])
        p.open()

    def show_room_popup(self):
        p = HugePopup(first_button=partial(self.set_table, 'room'),
                      second_button=partial(self.set_table, 'rooms'),
                      **popup_data['room'])
        p.open()

    def show_login_popup(self):
        p = LoginPopup(accept=self.login)
        p.open()


class LessonBar(ActionBar):
    pass


class MenuApp(App):
    def build(self):
        # basic_layout = BoxLayout(orientation='vertical')
        #
        # # menu_layout = BoxLayout(size_hint_y=0.08, spacing=2)
        # # buttons = [Button(text="button%d" % (i + 1)) for i in range(6)]
        # # buttons[0].bind(on_press=self.show_group_popup)
        # # for i in range(6):
        # #     menu_layout.add_widget(buttons[i])
        #
        # lesson_set = [[data_lesson[int(random() * 100) % 2]
        #                for i in range(5)] for j in range(6)]
        # table = lesson_table_creator(lesson_set=lesson_set)
        # basic_layout.add_widget(table)

        menu = MainWindow(table_type='groups')
        return menu


if __name__ == "__main__":
    Builder.load_file('./schedule.kv')
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    MenuApp().run()
