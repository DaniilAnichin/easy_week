#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.app import App

# Data which will form the view of pair, e.g. week days, time lapse
# Division may be useful for translation
day_times = [
    '08:30 - 10:05',
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
# Test data for lessons, just example
data_pair = [dict(teacher='Orlovskiy I.V.', lesson='High Math II',
                  type=lesson_types.index('Lecture'),
                  groups=['IK-51', 'IK-52'], room='18/413',
                  week_time={'week': 'upper', 'day': 1, 'number': 1}),
             dict(teacher='Lisovichenko O.I.', lesson='OOP',
                  type=lesson_types.index('Practice'),
                  groups=['IK-51'], room='18/438',
                  week_time={'week': 'lower', 'day': 4, 'number': 3})]


class Lesson(Button):
    def __init__(self, **kwargs):
        self.teacher = kwargs['teacher']
        self.lesson = kwargs['lesson']
        self.type = kwargs['type']
        self.groups = kwargs['groups']
        self.room = kwargs['room']
        self.week_time = kwargs['week_time']
        self.text = self.__str__()
        self.on_press = kwargs['on_press']
        super(Button, self).__init__()
        # super(Label, self).__init__(**kwargs)

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


def clickable():
    print 'And this too!'


class LessonsApp(App):
    def build(self):
        button = Factory.Lesson(on_press=clickable,
                                **data_pair[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
