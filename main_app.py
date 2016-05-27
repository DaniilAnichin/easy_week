#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Main window for easy week, includes Action bar and logging
"""
import gettext

eng = gettext.translation('easy_week', './locale', languages=['en'])
ua = gettext.translation('easy_week', './locale', languages=['ua'])
ru = gettext.translation('easy_week', './locale', languages=['ru'])

ua.install()
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.properties import ListProperty, OptionProperty, ObjectProperty, \
    StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.app import App
from schedule import LessonTable
from lessons import week_types
from popups import ChoicePopup, LoginPopup, popup_data
from database import collect_lessons, group_list, teacher_list, room_list, \
    day_num, lesson_num


class MainWindow(BoxLayout):
    lesson_set = ListProperty()
    day_num = NumericProperty(day_num)
    lesson_num = NumericProperty(lesson_num)
    week = OptionProperty('upper', options=['upper', 'lower'])
    table_type = OptionProperty('teacher', options=['group', 'teacher', 'room'])
    content = StringProperty(unicode('вик. Міхнєва Ю. Р.', 'utf-8'))
    table = ObjectProperty()
    log_label = ObjectProperty(None)
    title = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.set_table()

    def set_table(self, table_type=None, content=None, week=None):
        self.log_label.text = _('Preparing data')
        if week is not None:
            self.week = week

        if table_type is not None:
            self.table_type = table_type

        if content is not None:
            if self.table_type is 'group' and content not in group_list:
                self.log_label.text = _('Wrong group passed: %s') % content
                return -1
            if self.table_type is 'teacher' and content not in teacher_list:
                self.log_label.text = _('Wrong teacher passed: %s') % content
                return -1
            if self.table_type is 'room' and content not in room_list:
                self.log_label.text = _('Wrong room passed: %s') % content
                return -1
            # black magic
            # .encode('utf-8').decode('utf-8')
            self.content = content

        self.clear_table()
        self.lesson_set = collect_lessons(
            content_type=self.table_type,
            content=self.content
        )

        if len(self.lesson_set) is not 0:
            if self.week is 'upper':
                lesson_table = LessonTable(
                    lesson_set=self.lesson_set[:self.day_num],
                    cap_text=week_types[self.week]
                )
            else:
                lesson_table = LessonTable(
                    lesson_set=self.lesson_set[self.day_num:],
                    cap_text=week_types[self.week]
                )
            self.title.title = _('%s schedule, %s week').decode('utf-8') % \
                               (self.content, week_types[self.week])
            self.log_label.text = self.title.title
            self.table.add_widget(lesson_table)
        else:
            self.log_label.text = _('Troubles loading schedule')

    def clear_table(self):
        if isinstance(self.table, BoxLayout):
            self.table.clear_widgets()

    def switch_week(self):
        self.week = 'upper' if self.week == 'lower' else 'lower'
        self.clear_table()
        self.set_table()

    def login(self, login, password):
        # if users['login'].password == password: (from db)
        # self.user = ...
        self.log_label.text = _('You have logged in as %s').decode(
            'utf-8') % login
        # else:
        #     self.log_label.text = 'Incorrect password, try again'

    # Helpful functions
    def logout(self):
        # self.user = ...
        self.log_label.text = _('You have logged out')

    def show_group_popup(self):
        ChoicePopup(on_release=partial(self.set_table, 'group'),
                    choices=group_list,
                    **popup_data['group']).open()

    def show_teacher_popup(self):
        ChoicePopup(on_release=partial(self.set_table, 'teacher'),
                    choices=teacher_list,
                    **popup_data['teacher']).open()

    def show_room_popup(self):
        ChoicePopup(on_release=partial(self.set_table, 'room'),
                    choices=room_list,
                    **popup_data['room']).open()

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
