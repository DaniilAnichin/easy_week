#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
All necessary table definitions for Easy Week
"""
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.magnet import Magnet
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
from lessons import week_days, day_times

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
        return result


class DraggableLesson(Magnet):
    m_lesson = ObjectProperty(None, force_dispatch=True)

    def __init__(self, **kwargs):
        super(DraggableLesson, self).__init__(**kwargs)
        self.duration = 0.5
        Clock.schedule_once(lambda *x: self.add_widget(self.m_lesson), 0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.m_lesson.size = self.m_lesson.size
            self.m_lesson.size_hint = (None, None)
            self.remove_widget(self.m_lesson)
            self.parent.parent.add_widget(self.m_lesson)
            self.center = touch.pos
            self.m_lesson.center = touch.pos
            return True

        return super(DraggableLesson, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        boxes = self.parent.parent.children

        if touch.grab_current == self:
            self.m_lesson.center = touch.pos
            for box in boxes:
                if isinstance(box, LessonHolder) and \
                        box.collide_point(*touch.pos):
                    self.parent.remove_widget(self)
                    box.add_widget(self)

        return super(DraggableLesson, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.parent.parent.remove_widget(self.m_lesson)
            self.add_widget(self.m_lesson)
            touch.ungrab(self)
            return True

        return super(DraggableLesson, self).on_touch_up(touch)


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
        for day in range(self.day_num):
            for number in range(self.lesson_num):
                lesson = self.lesson_set[day][number]
                box = LessonHolder(day=day, number=number)
                box.size_hint = (
                    (1 - ruler_hint) / self.day_num,
                    (1 - ruler_hint) / self.lesson_num
                )
                box.pos_hint = {
                    'x': ruler_hint + day * (1 - ruler_hint) / self.day_num,
                    'y': 1 - ruler_hint - (number + 1) *
                                          (1 - ruler_hint) / self.lesson_num}

                box.add_widget(DraggableLesson(m_lesson=lesson))
                self.add_widget(box)

        # Filling table with rulers-buttons(labels, in future)
        for day in range(self.day_num):
            button = KindaButton(
                text=week_days[day],
                size_hint=((1 - ruler_hint) / self.day_num, ruler_hint),
                pos_hint={
                    'x': ruler_hint + day * (1 - ruler_hint) / self.day_num,
                    'y': 1 - ruler_hint
                }
            )
            self.add_widget(button)

        for number in range(self.lesson_num):
            button = KindaButton(
                text='\n'.join(day_times[number].split(' - ')),
                size_hint=(ruler_hint, (1 - ruler_hint) / self.lesson_num),
                pos_hint={
                    'x': 0,
                    'y': (1 - ruler_hint) * (1-(number + 1.) / self.lesson_num)
                }
            )
            self.add_widget(button)

        # Adding cap
        button = KindaButton(
            text=self.cap_text,
            size_hint=(ruler_hint, ruler_hint),
            pos_hint={'x': 0, 'y': 1 - ruler_hint}
        )
        self.add_widget(button)

    def clear_table(self):
        for child in self.children:
            if isinstance(child, LessonHolder):
                for grandchild in child.children:
                    grandchild.clear_widgets()


class ScheduleApp(App):
    def build(self):
        pass


if __name__ == '__main__':
    Builder.load_file('./lessons.kv')
    Builder.load_file('./popups.kv')
    ScheduleApp().run()
