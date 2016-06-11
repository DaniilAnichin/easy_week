#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week m_lesson structure
"""
from kivy.uix.button import Button
from kivy.properties import *
from kivy.app import App
from text_data import data_lesson, lesson_to_str

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


class Lesson(Button):
    _db_id = NumericProperty()
    teacher = StringProperty('')
    lesson = StringProperty('')
    groups = ListProperty()
    room = StringProperty('')
    type = OptionProperty('pract', options=['lect', 'pract', 'lab'])
    week = OptionProperty('lower', options=['lower', 'upper'])
    day = BoundedNumericProperty(0, min=0, max=5)
    number = BoundedNumericProperty(0, min=0, max=4)
    lines = NumericProperty(1)
    view_type = OptionProperty(
        'empty', options=['group', 'teacher', 'room', 'empty']
    )

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))

    def __str__(self):
        # Change color due to the lesson type
        if not self.empty():
            self.background_color = lesson_colors[self.type]
        return lesson_to_str(self)

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
