#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week m_lesson structure
"""
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.behaviors.drag import DragBehavior
from kivy.properties import *
from kivy.app import App
from text_data import data_lesson, lesson_to_str, lesson_types, week_days, \
    day_times

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
    update = ObjectProperty()

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))
        bind_data = {key: self.redraw for key in self.__dict__().keys()}
        self.bind(**bind_data)

    def __str__(self):
        # Change color due to the lesson type
        if not self.empty():
            self.background_color = lesson_colors[self.type]
        return lesson_to_str(self)

    def on_release(self):
        LessonPopup(lesson=self).open()

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
        result = self.teacher == '' or self.room == '' or self.lesson == ''
        return result

    def __dict__(self):
        data = dict(
            teacher=self.teacher,
            lesson=self.lesson,
            groups=self.groups,
            room=self.room,
            type=self.type,
            week=self.week,
            day=self.day,
            view_type=self.view_type,
            update=self.update
        )
        return data

    def redraw(self, *args):
        self.text = self.__str__()
        self.lines = len(self.text.split('\n'))


class ChoiceInput(TextInput):
    choices = ListProperty()
    drop_down = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChoiceInput, self).__init__(**kwargs)
        self.drop_down = DropDown()
        self.bind(focus=self.on_focus)
        self.drop_down.bind(
            on_select=lambda instance, x: setattr(self, 'text', x)
        )

    def make_drop_down(self, *args):
        self.drop_down.clear_widgets()
        for choice in self.choices:
            if self.text in choice or self.text == '':
                button = Button(
                    text=choice,
                    size_hint_y=None,
                    height=35
                )
                button.bind(
                    on_release=lambda btn: self.drop_down.select(btn.text)
                )
                self.drop_down.add_widget(button)
        if len(self.drop_down.children) > 0:
            self.drop_down.open(self)

    def on_focus(self, *args):
        self.bind(text=self.make_drop_down)


class LessonPopup(Popup):
    """
    Popup form for editing the lesson object
    """
    lesson = ObjectProperty()
    new_lesson = ObjectProperty()
    group_input = ObjectProperty()
    teacher_input = ObjectProperty()
    lesson_input = ObjectProperty()
    type_input = ObjectProperty()
    room_input = ObjectProperty()
    day_input = ObjectProperty()
    time_input = ObjectProperty()
    first_week = ObjectProperty()
    second_week = ObjectProperty()

    def __init__(self, **kwargs):
        super(LessonPopup, self).__init__(**kwargs)

    def update(self):
        self.new_lesson = Lesson(
            teacher=self.teacher_input.text,
            lesson=self.lesson_input.text.encode('utf-8'),
            groups=self.group_input.text.encode('utf-8').split(', '),
            room=self.room_input.text.encode('utf-8'),
            week=('lower' if self.second_week.state == 'down' else 'upper'),
            day=week_days.index(self.day_input.text.encode('utf-8')),
            number=day_times.index(self.time_input.text),
            view_type=self.lesson.view_type
        )
        if self.second_week.state == self.first_week.state == 'up':
            pass
        for _type in lesson_types.keys():
            if lesson_types[_type] == self.type_input.text.encode('utf-8'):
                self.new_lesson.type = _type
        self.lesson.update(
            old_lesson=self.lesson,
            new_lesson=self.new_lesson
        )
        data = self.new_lesson.__dict__()
        for key in data.keys():
            if key != 'update':
                setattr(self.lesson, key, data[key])


class LessonsApp(App):
    def build(self):
        button = Lesson(**data_lesson[0])
        return button


if __name__ == "__main__":
    LessonsApp().run()
