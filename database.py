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
week_num = week_len * day_len

teacher_list = [teacher.decode('cp1251')[:-1] for teacher
                in open('./db/_Teachers.txt', 'rt').readlines()]

group_list = [group[:-1] for group in open('./db/dihc.txt', 'rt').readlines()]

room_list = []


type_dict = {
    unicode('Лек', 'utf-8'): 'lect',
    unicode('Лаб', 'utf-8'): 'lab',
    unicode('Прак', 'utf-8'): 'pract'
}


def get_groups(stream):
    result = []
    for group in group_list:
        if group.startswith(stream):
            result.append(group)
    return result


def collect_lessons(content_type, **kwargs):
    lesson_set = [[None for i in range(day_len)] for j in range(week_len * 2)]
    if content_type == 'teacher':
        teacher = Tools_for_db.Teacher(name=kwargs['content'])
        for i in range(week_num * 2):
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
                                   week=('upper' if i < week_num else 'lower'),
                                   day=(i / day_len % week_len),
                                   number=(i % day_len))
                lesson_set[int(i / day_len)][(i % day_len)] = my_lesson
            else:
                lesson_set[int(i / day_len)][(i % day_len)] = Lesson(
                    teacher=kwargs['content'].encode('utf-8'),
                    week=('upper' if i < week_num else 'lower'),
                    day=(i / day_len % week_len),
                    number=(i % day_len)
                )
    elif content_type == 'group':
        group = Tools_for_db.Group(name=kwargs['content'])
        for i in range(week_num * 2):
            lesson = group.getInfoByTime(i)
            print lesson
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                type = type_dict[lesson[2]]
                teach = get_groups(lesson[3])
                my_lesson = Lesson(teacher=teach.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=type,
                                   groups=group.name,
                                   room=str(int(room)),
                                   week=('upper' if i < week_num else 'lower'),
                                   day=(i / day_len % week_len),
                                   number=(i % day_len))
                lesson_set[int(i / day_len)][(i % day_len)] = my_lesson
            else:
                lesson_set[int(i / day_len)][(i % day_len)] = Lesson(
                    groups=group.name,
                    week=('upper' if i < week_num else 'lower'),
                    day=(i / day_len % week_len),
                    number=(i % day_len)
                    )
    elif content_type == 'room':
        pass
    else:
        print 'Oops..'
    return lesson_set


if __name__ == '__main__':
    name = getTeacher(57)
    collect_lessons('group', content=group_list[58])
