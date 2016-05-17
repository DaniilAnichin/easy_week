#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, OptionProperty, \
    BoundedNumericProperty, NumericProperty
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
lesson_types = {
    'lect': 'Lecture',
    'pract': 'Practice',
    'lab': 'Laboratory'
}
week_types = {
    'upper': 'upper',
    'lower': 'lower'
}
week_days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]
# Test popup_data for lessons, just example
data_lesson = [dict(teacher='Orlovskiy I.V.', lesson='High Math II',
                    type='lect', groups=['IK-51', 'IK-52'], room='18/413',
                    week='upper', day=1, number=1),
               dict(teacher='Lisovichenko O.I.', lesson='OOP',
                    type='pract', groups=['IK-51'], room='18/438',
                    week='lower', day=4, number=3)]


class Lesson(Button):
    teacher = StringProperty()
    lesson = StringProperty()
    groups = ListProperty()
    room = StringProperty()
    type = OptionProperty('pract', options=["lect", "pract", "lab"])
    week = OptionProperty('lower', options=['lower', 'upper'])
    day = BoundedNumericProperty(0, min=0, max=5)
    number = BoundedNumericProperty(0, min=0, max=4)
    lines = NumericProperty(1)

    def __init__(self, view_type='All', **kwargs):
        super(Button, self).__init__(**kwargs)
        self.text = self.__str__(view_type)
        self.lines = len(self.text.split('\n'))

    def __str__(self, *args):
        result = 'Here You have:'
        result += '\nAn %s %s' % (self.lesson, lesson_types[self.type])
        result += '\nWith %s' % self.teacher
        result += '\nIn %s room' % self.room
        result += '\nGroups: ' + ', '.join(self.groups)
        result += '\nAt %s week' % week_types[self.week]
        result += '\n%s (%s)' % (week_days[self.day], day_times[self.number])
        return result


def clickable(b):
    # print 'And this too!({})'.format(b.height / (len(b.text.split('\n')) + 2))
    print 'And this too!({})'.format(b)


class LessonsApp(App):
    def build(self):
        button = Lesson(on_press=clickable,
                        **data_lesson[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
