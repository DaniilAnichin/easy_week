#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionButton
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.app import App
import lessons
import popups
import main_app
Builder.load_file('./lessons.kv')
Builder.load_file('./popups.kv')


class LessonBar(ActionBar):
    @staticmethod
    def show_group_popup(b):
        p = Factory.HugePopup(first_button=main_app.MenuApp.set_group(),
                              second_button=None,
                              **popups.data_group)
        p.open()

    @staticmethod
    def show_teacher_popup(b):
        p = Factory.HugePopup(first_button=main_app.MenuApp.set_group(),
                              second_button=None,
                              **popups.data_teacher)
        p.open()

    @staticmethod
    def show_room_popup(b):
        p = Factory.HugePopup(first_button=main_app.MenuApp.set_group(),
                              second_button=None,
                              **popups.data_room)
        p.open()


class LessonDay(BoxLayout):
    def __init__(self, **kwargs):
        self.lesson_set = kwargs['lesson_set']
        super(BoxLayout, self).__init__(**kwargs)
        for i in self.lesson_set:
            pass


class LessonTable(BoxLayout):
    def __init__(self, **kwargs):
        # lesson_set = kwargs['lesson_set']
        # for i in range(len(lesson_set)):
        #     row_box = BoxLayout(orientation='vertical')
        #     for j in range(len(lesson_set[0])):
        #         lesson = lessons.Lesson(**lesson_set[i][j])
        #         button = Factory.Lesson(text=lesson.__str__())
        #         row_box.add_widget(button)
        #     self.add_widget(row_box)
        self.lesson_set = kwargs['lesson_set']
        super(BoxLayout, self).__init__(**kwargs)


def lesson_table_creator(lesson_set, **kwargs):
    holder = BoxLayout(**kwargs)
    for i in range(len(lesson_set)):
        row_box = BoxLayout(orientation='vertical')
        for j in range(len(lesson_set[0])):
            lesson = Factory.Lesson(on_press=lessons.clickable,
                                    **lesson_set[i][j])
            row_box.add_widget(lesson)
        holder.add_widget(row_box)

    return holder


class ScheduleApp(App):
    def build(self):
        self.title = "Schedule, mf"
        hour_box = lesson_table_creator([[lessons.data_pair[0] for i in range(4)]
                                         for j in range(5)])
        # hour_box = Factory.LessonTable(lesson_set=[[lessons.data_pair[0]
        #                                    for i in range(4)]
        #                                    for j in range(5)])
        return hour_box


if __name__ == '__main__':
    ScheduleApp().run()
