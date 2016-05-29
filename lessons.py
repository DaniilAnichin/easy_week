#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.uix.behaviors.drag import DragBehavior
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
    'lect': _('Lecture'),
    'pract': _('Practice'),
    'lab': _('Laboratory')
}
week_types = {
    'upper': 'I',
    'lower': 'II'
}
week_days = [
    _('Monday'),
    _('Tuesday'),
    _('Wednesday'),
    _('Thursday'),
    _('Friday'),
    _('Saturday'),
    _('Sunday')
]
colors = {
    'red': [1, 0, 0, 1],
    'green': [0, 1, 0, 1],
    'yellow': [0, 1, 1, 1],
    'blue': [0, 0, 1, 1],
    'orange': [0.9, 0.9, 0.0, 1],
    'pink': [1, 0.71, 0.75, 1]
}
lesson_colors = {
    'lect': colors['blue'],
    'pract': colors['green'],
    'lab': colors['red']
}
# Test popup_data for lessons, just example
data_lesson = [dict(teacher='Orlovskiy I.V.', lesson='High Math II',
                    type='lect', groups=['IK-51', 'IK-52'], room='18/413',
                    week='upper', day=1, number=1),
               dict(teacher='Lisovichenko O.I.', lesson='OOP',
                    type='pract', groups=['IK-51'], room='18/438',
                    week='lower', day=4, number=3)]


class Lesson(DragBehavior, Button):
    teacher = StringProperty()
    lesson = StringProperty()
    groups = ListProperty()
    room = StringProperty()
    type = OptionProperty('pract', options=['lect', 'pract', 'lab'])
    week = OptionProperty('lower', options=['lower', 'upper'])
    day = BoundedNumericProperty(0, min=0, max=5)
    number = BoundedNumericProperty(0, min=0, max=4)
    lines = NumericProperty(1)
    view_type = OptionProperty('empty', options=['group', 'teacher', 'room',
                                                 'empty'])

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))

    def __str__(self):
        # Change color due to the lesson type
        if self.view_type == 'empty':
            return ''
        self.background_color = lesson_colors[self.type]
        result = '%s' % self.lesson.decode('utf-8')[:12].encode('utf-8')
        if len(self.lesson.decode('utf-8')) > 12:
            result += '...'
        # result += '\n%s' % lesson_types[self.type]
        if not self.view_type.startswith('teacher'):
            result += '\n%s' % self.teacher.decode('utf-8')[:12].encode('utf-8')
            if len(self.teacher.decode('utf-8')) > 12:
                result += '...'
        if not self.view_type.startswith('room'):
            result += _('\nIn %s room') % self.room
        if not self.view_type.startswith('group'):
            groups = ', '.join(self.groups)
            result += '\n%s' % groups[:14] + ('...' if len(groups) > 17 else '')
        return result

    def __eq__(self, other):
        result = True
        if self.teacher != other.teacher:
            result = False
        if self.lesson != other.lesson:
            result = False
        if self.groups != other.groups:
            result = False
        if self.room != other.room:
            result = False
        if self.type != other.type:
            result = False
        return result

    def empty(self):
        return self.view_type == 'empty'


class LessonsApp(App):
    def build(self):
        button = Lesson(**data_lesson[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
