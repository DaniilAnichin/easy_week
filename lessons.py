#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.uix.behaviors.focus import FocusBehavior
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


class Lesson(FocusBehavior, Button):
    teacher = StringProperty()
    lesson = StringProperty()
    groups = ListProperty()
    room = StringProperty()
    type = OptionProperty('pract', options=['lect', 'pract', 'lab'])
    week = OptionProperty('lower', options=['lower', 'upper'])
    day = BoundedNumericProperty(0, min=0, max=5)
    number = BoundedNumericProperty(0, min=0, max=4)
    lines = NumericProperty(1)
    view_type = OptionProperty('group', options=['group', 'teacher', 'room'])

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))

    def __str__(self):
        result = '%s...' % self.lesson.decode('utf-8')[:12].encode('utf-8')
        result += '\n%s' % lesson_types[self.type]
        if not self.view_type.startswith('teacher'):
            result += '\n%s...' % self.teacher.decode('utf-8')[:12].encode('utf-8')
        if not self.view_type.startswith('room'):
            result += '\nIn %s room' % self.room
        if not self.view_type.startswith('group'):
            result += '\n%s...' % ', '.join(self.groups)[:17]
        # if not self.view_type.endswith('s'):
        #     result += '\nAt %s week' % week_types[self.week]
        #     result += '\n%s, %s' % (week_days[self.day], day_times[self.number])
        return result


def lesson_click(b):
    # test function, will die soon
    print 'And this too!({})'.format(b.lesson)


class LessonsApp(App):
    def build(self):
        button = Lesson(on_press=print_function, **data_lesson[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
