#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterPlaneLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.app import App
from lessons import lesson_click


class LessonTable(FloatLayout):
    lesson_set = ListProperty()
    day_num = NumericProperty(0)
    lesson_num = NumericProperty(0)

    def __init__(self, **kwargs):
        super(LessonTable, self).__init__(**kwargs)
        self.day_num = len(self.lesson_set)
        self.lesson_num = len(self.lesson_set[0])

        for i in range(self.day_num):
            for j in range(self.lesson_num):
                lesson = self.lesson_set[i][j]
                # lesson.size_hint = (None, None)
                lesson.size_hint = (1 / self.day_num,
                                    1 / self.lesson_num)
                # lesson.size = (self.width / self.day_num,
                #                self.height / self.lesson_num)
                # lesson.size = (120, 80)
                lesson.pos_hint = {'x': i / self.day_num,
                                   'y': j / self.lesson_num}
                self.add_widget(self.lesson_set[i][j])


class LayoutsApp(App):
    def build(self):
        # lesson_table = LessonWeek(day_set=[
        #     LessonDay(lesson_set=[Lesson(on_release=lesson_click,
        #                                  view_type='all',
        #                                  **data_lesson[0])
        #                           for i in range(5)
        #                           ]) for j in range(6)])
        # lesson_table = LessonTable(lesson_set=[[Button(text='Oh no, %d %d' % (i, j))
        #                                        for i in range(5)]
        #                                        for j in range(6)])
        # box = BoxLayout(size_hint=(1, 1))
        # box.add_widget(lesson_table)
        # return box
        f = FloatLayout()
        # f.size_hint = None, None
        # f.size = (600, 600)
        lesson_set = [[Button(text='Oh no, %d %d' % (i, j))
                      for i in range(5)]
                      for j in range(6)]
        day_num = len(lesson_set)
        print day_num
        lesson_num = len(lesson_set[0])
        print lesson_num
        for i in range(day_num):
            for j in range(lesson_num):
                lesson = Button(text='Oh no, %d %d' % (i, j))
                lesson.size_hint = (1. / day_num,
                                    1. / lesson_num)
                # print (1 / day_num, 1. / lesson_num)

                lesson.pos_hint = {'x': float(i) / day_num,
                                   'y': float(j) / lesson_num}
                f.add_widget(lesson)
        return f


if __name__ == '__main__':
    LayoutsApp().run()
