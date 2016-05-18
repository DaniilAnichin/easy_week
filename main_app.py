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
from database import collect_lessons


class NoOverScroll(ScrollEffect):
    pass


class MainWindow(BoxLayout):
    lesson_set = ListProperty()
    log_label = ObjectProperty(None)
    table_type = OptionProperty('teacher', options=['groups', 'group',
                                                    'teachers', 'teacher',
                                                    'rooms', 'room'])
    content = StringProperty(unicode('вик. Міхнєва Ю. Р.', 'utf-8'))
    scroll_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.no_resize = False
        self.scroll_layout.effect_cls = NoOverScroll
        self.log_label.text = 'loading database...(wait a bit, pls)'
        self.load_database()

    def load_database(self):
        self.lesson_set = collect_lessons(content_type=self.table_type,
                                          content=self.content)[:6]
        self.log_label.text = 'Database loaded successfully'
        self.set_table()

    def set_table(self, table_type=None, content=None):
        self.log_label.text = 'Preparing data'
        self.clear_table()

        if table_type is not None:
            self.table_type = table_type

        if content is not None:
            self.content = content #.encode('utf-8').decode('utf-8')   # black magic

        self.lesson_set = collect_lessons(content_type=self.table_type,
                                          content=self.content)[:6]

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
            day_set = [LessonDay(lesson_set=day) for day in self.lesson_set]
            lesson_table = LessonWeek(day_set=day_set)

        self.log_label.text = 'Showing %s table' % self.table_type
        self.log_label.text += ' for %s' % self.content if self.content is not None else ''
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
        menu = MainWindow()
        return menu


if __name__ == "__main__":
    Builder.load_file('./schedule.kv')
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    MenuApp().run()
