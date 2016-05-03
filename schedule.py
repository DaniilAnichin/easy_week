#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
import lessons


class LessonDay(BoxLayout):
    def __init__(self, **kwargs):
        self.lesson_set = kwargs['lesson_set']
        super(BoxLayout, self).__init__(**kwargs)


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


def lesson_table_creator(pair_set, **kwargs):
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
        # hour_box = lesson_table_creator([[lessons.data_pair[0] for i in range(4)]
        #                                  for j in range(5)])
        hour_box = Factory.LessonTable(lesson_set=[[lessons.data_pair[0]
                                           for i in range(4)]
                                           for j in range(5)],
                               size_hint=(None, None),
                               size=(800, 600))
        return hour_box


if __name__ == '__main__':
    ScheduleApp().run()
