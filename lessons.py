#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App

day_times = [
    '8:30 - 10:05',
    '10:25 - 12:00',
    '12:20 - 13:55',
    '14:15 - 15:50',
    '16:10 - 17:45'
]
lesson_types = [
    'Lecture',
    'Practice',
    'Laboratory',
    'Other'
]
week_days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]


class Lesson:
    def __init__(self, **kwargs):
        self.teacher = kwargs['teacher']
        self.lesson = kwargs['lesson']
        self.type = kwargs['type']
        self.groups = kwargs['groups']
        self.room = kwargs['room']
        self.week_time = kwargs['week_time']

    def __str__(self, *excepted):
        result = 'Here You have:'
        result += '\nAn %s %s' % (self.lesson, lesson_types[self.type])
        result += '\nWith %s' % self.teacher
        result += '\nIn %s room' % self.room
        result += '\nGroups: ' + ', '.join(self.groups)
        result += '\nAt %s week' % self.week_time['week']
        result += '\n%s (%s)' % (week_days[self.week_time['day']],
                                 day_times[self.week_time['number']])
        return result


data_pair = [dict(teacher='Orlovskiy I.V.', lesson='High Math II',
                  type=lesson_types.index('Lecture'),
                  groups=['IK-51', 'IK-52'], room='18/413',
                  week_time={'week': 'upper', 'day': 1, 'number': 1}),
             dict(teacher='Lisovichenko O.I.', lesson='OOP',
                  type=lesson_types.index('Practice'),
                  groups=['IK-51'], room='18/438',
                  week_time={'week': 'lower', 'day': 4, 'number': 3})]


class ExampleApp(App):
    def build(self):
        lesson = Lesson(**data_pair[0])
        button = Button(text=lesson.__str__(),
                        text_size=(200, 200))
        return button


if __name__ == "__main__":
    ExampleApp().run()
