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
from lessons import Lesson
from text_data import week_days, day_times, data_lesson

ruler_hint = 0.08


class KindaButton(Button):
    pass


class LessonHolder(BoxLayout):
    day = NumericProperty()
    number = NumericProperty()

    def add_widget(self, widget, index=0):
        if widget.m_lesson:
            widget.m_lesson.day = self.day
            widget.m_lesson.number = self.number
        return super(BoxLayout, self).add_widget(widget, index)


class DraggableLesson(Magnet):
    old_parent = ObjectProperty(None)
    m_lesson = ObjectProperty(None, force_dispatch=True)
    table = ObjectProperty(None)

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
            if not self.table:
                self.table = self.parent.parent
            self.old_parent = self.parent
            self.table.add_widget(self.m_lesson)
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
                    if self.parent is not box:
                        self.parent.remove_widget(self)
                        box.add_widget(self)

        return super(DraggableLesson, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.table.remove_widget(self.m_lesson)
            self.add_widget(self.m_lesson)
            touch.ungrab(self)
            self.table.switch_lessons(self.parent, self.old_parent)
            return True

        return super(DraggableLesson, self).on_touch_up(touch)

    def collide_point(self, x, y):
        x_left = self.center_x - (self.width / 2.0)
        x_right = self.center_x
        y_bottom = self.center_y - (self.height / 2.0)
        y_top = self.center_y + (self.height / 2.0)
        return x_left <= x <= x_right and y_bottom <= y <= y_top


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
                box = LessonHolder(
                    day=day, number=number, orientation='vertical'
                )
                box.size_hint = (
                    (1 - ruler_hint) / self.day_num,
                    (1 - ruler_hint) / self.lesson_num
                )
                box.pos_hint = {
                    'x': ruler_hint + day * (1 - ruler_hint) / self.day_num,
                    'y': 1 - ruler_hint - (number + 1) *
                                          (1 - ruler_hint) / self.lesson_num}
                # if not lesson.empty():
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

    # def save_table(self, temp):
    #     print 'Table saved'

    def switch_lessons(self, holder, old_holder):
        # run popup, get result, blah blah
        draggable = holder.children[-1]   # lesson to move back
        holder.remove_widget(draggable)
        if holder.children and not (holder.children[0].m_lesson.empty() or
                                    draggable.m_lesson.empty()):
            new_less = holder.children[0].m_lesson
            old_less = Lesson(**new_less.__dict__())
            setattr(old_less, 'day', old_holder.day)
            setattr(old_less, 'number', old_holder.number)
            result = draggable.m_lesson.switch(draggable.m_lesson, old_less)
        elif holder.children and not holder.children[0].m_lesson.empty():
            new_less = holder.children[0].m_lesson
            old_less = Lesson(**new_less.__dict__())
            setattr(old_less, 'day', old_holder.day)
            setattr(old_less, 'number', old_holder.number)
            result = new_less.update(old_less, new_less)
        elif not draggable.m_lesson.empty():
            from_drag_with_time = Lesson(**draggable.m_lesson.__dict__())
            setattr(from_drag_with_time, 'day', old_holder.day)
            setattr(from_drag_with_time, 'number', old_holder.number)
            result = draggable.m_lesson.update(draggable.m_lesson, from_drag_with_time)
        else:
            result = 0
        old_holder.add_widget(draggable)
        if result:
            self.parent.parent.log_label.text = str(result)
            old_drag = old_holder.children[0]
            old_holder.remove_widget(old_drag)
            new_drag = holder.children[0]
            holder.remove_widget(new_drag)
            old_holder.add_widget(new_drag)
            holder.add_widget(old_drag)


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
