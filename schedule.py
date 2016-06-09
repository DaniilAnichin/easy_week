#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, \
    StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
from lessons import data_lesson, Lesson, week_days, day_times

ruler_hint = 0.08


class KindaButton(Button):
    pass


class LessonHolder(BoxLayout):
    day = NumericProperty()
    number = NumericProperty()

    def has_inside(self, lesson_center):
        result = True
        print 'Lesson center: ', lesson_center
        if 2 * abs(self.x - lesson_center[0]) > self.width:
            result = False
        if 2 * abs(self.y - lesson_center[1]) > self.height:
            result = False
        return False


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
                box = LessonHolder()
                box.size_hint = ((1 - ruler_hint) / self.day_num,
                                    (1 - ruler_hint) / self.lesson_num)
                box.pos_hint = {
                    'x': ruler_hint + i * (1 - ruler_hint) / self.day_num,
                    'y': 1 - ruler_hint - (j + 1) *
                                          (1 - ruler_hint) / self.lesson_num}

                # lesson.size_hint = ((1 - ruler_hint) / self.day_num,
                #                     (1 - ruler_hint) / self.lesson_num)
                # lesson.pos_hint = {
                #     'x': ruler_hint + i * (1 - ruler_hint) / self.day_num,
                #     'y': 1 - ruler_hint - (j + 1) *
                #                           (1 - ruler_hint) / self.lesson_num}
                box.add_widget(lesson)
                self.add_widget(box)
                lesson.bind(pos=self.move_lesson)

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

        # Clock.schedule_once(lambda dt: self.set_lesson_pos(), 1)

    def set_lesson_pos(self):
        for i in range(self.day_num):
            for j in range(self.lesson_num):
                lesson = self.lesson_set[i][j]
                lesson.pos_hint.pop('x')
                lesson.pos_hint.pop('y')
                lesson.pos = (
                    self.width * (ruler_hint + i * (1 - ruler_hint) / self.day_num),
                    self.height * (1 - ruler_hint - (j + 1) *
                                   (1 - ruler_hint) / self.lesson_num)
                )

    def move_lesson(*args):
        for i in range(len(args)):
            print i, args[i]

        # for child in self.children:
        #     if isinstance(child, LessonHolder):
        #         if child.has_inside(lesson):
        #             print child


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
