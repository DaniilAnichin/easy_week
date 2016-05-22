#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.lang import Builder
from kivy.app import App
from lessons import lesson_click, data_lesson, Lesson

lesson_size = (150, 70)


class LessonBar(ActionBar):
    login_bind = ObjectProperty()
    login_button = ObjectProperty(None)
    update_button = ObjectProperty(None)
    logout_button = ObjectProperty(None)
    group_button = ObjectProperty(None)
    teacher_button = ObjectProperty(None)
    room_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ActionBar, self).__init__(**kwargs)


class LessonDay(BoxLayout):
    lesson_set = ListProperty()

    def __init__(self, **kwargs):
        super(LessonDay, self).__init__(**kwargs)
        for lesson in self.lesson_set:
            lesson.size_hint = 1, 1
            self.add_widget(lesson)


class LessonWeek(BoxLayout):
    day_set = ListProperty()

    def __init__(self, **kwargs):
        super(LessonWeek, self).__init__(**kwargs)
        for day in self.day_set:
            self.add_widget(day)


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
                lesson.size_hint = None, None
                lesson.size = (self.width / self.day_num,
                               self.height / self.lesson_num)
                lesson.pos_hint = {'x': i / self.day_num,
                                   'y': j / self.lesson_num}
                self.add_widget(lesson)


class ScheduleApp(App):
    def build(self):
        # lesson_table = LessonWeek(day_set=[
        #     LessonDay(lesson_set=[Lesson(on_release=lesson_click,
        #                                  view_type='all',
        #                                  **data_lesson[0])
        #                           for i in range(5)
        #                           ]) for j in range(6)])
        lesson_table = LessonTable(lesson_set=[[Lesson(on_release=lesson_click,
                                                       view_type='all',
                                                       **data_lesson[0])
                                               for i in range(5)]
                                               for j in range(5)])
        return lesson_table


if __name__ == '__main__':
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    ScheduleApp().run()
