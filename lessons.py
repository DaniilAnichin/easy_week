#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week lesson structure
"""
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label
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
    type = OptionProperty('pract', options=["lect", "pract", "lab"])
    week = OptionProperty('lower', options=['lower', 'upper'])
    day = BoundedNumericProperty(0, min=0, max=5)
    number = BoundedNumericProperty(0, min=0, max=4)
    lines = NumericProperty(1)
    view_type = OptionProperty('all', options=['groups', 'group',
                                               'teachers', 'teacher',
                                               'rooms', 'room', 'all'])

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))

    def __str__(self):
        result = 'An %s %s' % (self.lesson, lesson_types[self.type])
        if not self.view_type.startswith('teacher'):
            result += '\nWith %s' % self.teacher
        if not self.view_type.startswith('room'):
            result += '\nIn %s room' % self.room
        if not self.view_type.startswith('group'):
            result += '\nGroups: ' + ', '.join(self.groups)
        if not self.view_type.endswith('s'):
            result += '\nAt %s week' % week_types[self.week]
            result += '\n%s, %s' % (week_days[self.day], day_times[self.number])
        return result

    # def _on_focus(self, instance, value, *args):


class LessonBubble(Bubble):
    def __init__(self, lesson, **kwargs):
        super(LessonBubble, self).__init__(**kwargs)
        print 'PBubble started'
        my_bubble = Bubble(orientation='horizontal', pos=lesson.pos)
        my_bubble.arrow_pos = 'top_left'   # which is correct?
        data_label = Label(text='At %s week' % week_types[lesson.week])
        data_label.text += '\n%s, %s' % (week_days[lesson.day],
                                         day_times[lesson.number])
        if lesson.view_type.startswith('teacher'):
            data_label.text += '\nWith %s' % lesson.teacher
        if lesson.view_type.startswith('room'):
            data_label.text += '\nIn %s room' % lesson.room
        if lesson.view_type.startswith('group'):
            data_label.text += '\nGroups: ' + ', '.join(lesson.groups)

        my_bubble.add_widget(data_label)
        self.add_widget(my_bubble)


def lesson_click(b):
    # test function, will die soon
    print 'And this too!({})'.format(b.lesson)


class LessonsApp(App):
    def build(self):
        button = Lesson(on_press=LessonBubble, **data_lesson[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
