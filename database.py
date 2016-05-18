#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week database structure
"""
from random import random
from lessons import Lesson, lesson_click, data_lesson
from db import Tools_for_db
from db.BlakMagicAlogorithm import getTeacher

week_len = 6
day_len = 5

teacher_list = []
group_list = []
room_list = []


type_dict = {
    unicode('Лек', 'utf-8'): 'lect',
    unicode('Лаб', 'utf-8'): 'lab',
    unicode('Прак', 'utf-8'): 'pract'
}


def get_lesson_set():
    return [[Lesson(on_release=lesson_click,
                    **data_lesson[int(random() * 100) % 2])
            for i in range(60)] for j in range(70)]


def get_groups(stream):
    result = []
    with open('./db/dihc.txt', 'rt') as out:
        groups = out.readlines()
        for group in groups:
            if group.startswith(stream):
                result.append(group[:-1])
    return result


def collect_lessons(content_type, **kwargs):
    lesson_set = [[None for i in range(5)] for j in range(12)]
    if content_type == 'teacher':
        teacher = Tools_for_db.Teacher(name=kwargs['content'])
        for i in range(60):
            lesson = teacher.getInfoByTime(i)
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                type = type_dict[lesson[2]]
                groups = get_groups(lesson[3])
                my_lesson = Lesson(teacher=kwargs['content'].encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=type,
                                   groups=groups,
                                   room=str(int(room)),
                                   week=('upper' if i < 30 else 'lower'),
                                   day=(i / 5 % 6),
                                   number=(i % 5))
                lesson_set[int(i / 5)][(i % 5)] = my_lesson
            else:
                lesson_set[int(i / 5)][(i % 5)] = Lesson(
                    teacher=kwargs['content'].encode('utf-8'),
                    week=('upper' if i < 30 else 'lower'),
                    day=(i / 5 % 6),
                    number=(i % 5)
                    )
    elif content_type == 'group':
        pass
    elif content_type == 'room':
        pass
    else:
        print 'Oops..'
    return lesson_set


if __name__ == '__main__':
    name = getTeacher(57)
    collect_lessons('teacher', content=name)
