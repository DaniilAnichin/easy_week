#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, \
    StringProperty
from kivy.lang import Builder
from kivy.app import App
from lessons import data_lesson, Lesson, week_days, day_times

ruler_hint = 0.08


class KindaButton(Button):
    pass


class LessonTable(FloatLayout):
    lesson_set = ListProperty()
    day_num = NumericProperty(0)
    lesson_num = NumericProperty(0)
    double_week = BooleanProperty(False)
    cap_text = StringProperty()

    def __init__(self, **kwargs):
        super(LessonTable, self).__init__(**kwargs)
        self.day_num = len(self.lesson_set)
        self.lesson_num = len(self.lesson_set[0])

        # Filling table with lessons
        for i in range(self.day_num):
            for j in range(self.lesson_num):
                lesson = self.lesson_set[i][j]
                lesson.size_hint = ((1 - ruler_hint) / self.day_num,
                                    (1 - ruler_hint) / self.lesson_num)
                lesson.pos_hint = {
                    'x': ruler_hint + i * (1 - ruler_hint) / self.day_num,
                    'y': 1 - ruler_hint - (j + 1) *
                                          (1 - ruler_hint) / self.lesson_num}
                # lesson.bind(on_release=LessonPopup(lesson=lesson).open)

                self.add_widget(lesson)

        # Filling table with rulers-buttons(labels, in future)
        for i in range(self.day_num):
            button = KindaButton(
                text=week_days[i],
                size_hint=((1 - ruler_hint) / self.day_num, ruler_hint),
                pos_hint={'x': ruler_hint + i * (1 - ruler_hint) / self.day_num,
                          'y': 1 - ruler_hint},
            )
            self.add_widget(button)

        for j in range(self.lesson_num):
            button = KindaButton(
                text='\n'.join(day_times[j].split(' - ')),
                size_hint=(ruler_hint, (1 - ruler_hint) / self.lesson_num),
                pos_hint={'x': 0,
                          'y': (1 - ruler_hint)*(1-(j + 1.) / self.lesson_num)}
            )
            self.add_widget(button)

        # Adding cap
        button = KindaButton(
            text=self.cap_text,
            size_hint=(ruler_hint, ruler_hint),
            pos_hint={'x': 0,
                      'y': 1 - ruler_hint}
        )
        self.add_widget(button)


class ScheduleApp(App):
    def build(self):
        lesson_table = LessonTable(lesson_set=[[Lesson(**data_lesson[0])
                                                for i in range(5)]
                                               for j in range(6)],
                                   cap_text='cap')
        return lesson_table


if __name__ == '__main__':
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    ScheduleApp().run()
