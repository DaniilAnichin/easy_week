#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.actionbar import ActionBar
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.app import App
from schedule import LessonSet, LessonDay, LessonWeek, LessonTable, lesson_size
from lessons import data_lesson, Lesson, clickable
from popups import HugePopup, LoginPopup, popup_data


class NoOverscroll(ScrollEffect):
    pass


class MainWindow(BoxLayout):
    lesson_set = ListProperty()
    day_set = ListProperty()

    def __init__(self, lesson_set, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        # lesson_table = LessonTable(day_set=[LessonSet(lesson_set=day)
        #                                    for day in self.day_set])
        lesson_table = LessonTable(lesson_set=lesson_set,
                                   size_hint=(None, None),
                                   pos_hint={'top': 1, 'left': 1})
        lesson_table.bind(minimum_height=lesson_table.setter('height'))
        lesson_table.bind(minimum_width=lesson_table.setter('width'))
        scroll = ScrollView(pos_hint={'top': 1},
                            bar_color=(.0, .8, .9, .9),
                            bar_width=5,
                            effect_cls=NoOverscroll)
        scroll.add_widget(lesson_table)
        self.add_widget(scroll)

    # This part is for popups and their selection:
    def show_group(self, group):
        print 'Group: %s' % group

    def show_groups(self):
        print 'Groups'

    def show_teacher(self, teacher):
        print 'Teacher: %s' % teacher

    def show_teachers(self):
        print 'Teachers'

    def show_room(self, room):
        print 'Room: %s' % room

    def show_rooms(self):
        print 'Rooms'

    def accept(self, login, password):
        print 'Login: %s, Pass: %s' % (login, password)

    def show_group_popup(self):
        p = HugePopup(first_button=self.view_group,
                      second_button=self.view_groups,
                      **popup_data['data_group'])
        p.open()

    def show_teacher_popup(self):
        p = HugePopup(first_button=self.show_teacher,
                      second_button=self.show_teachers,
                      **popup_data['teacher'])
        p.open()

    def show_room_popup(self):
        p = HugePopup(first_button=self.show_room,
                      second_button=self.show_rooms,
                      **popup_data['room'])
        p.open()

    def show_login_popup(self):
        p = LoginPopup(accept=self.accept)


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

        menu = MainWindow(lesson_set=[[Lesson(on_release=clickable,
                                              **data_lesson[int(random() * 100) % 2])
                                      for i in range(30)] for j in range(30)])
        return menu


if __name__ == "__main__":
    Builder.load_file('./schedule.kv')
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    MenuApp().run()
