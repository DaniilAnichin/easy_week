#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week database structure
"""
import csv
from lessons import Lesson
from db import Tools_for_db
from db.BlakMagicAlogorithm import UnicodeReader
from db.Tools_for_db import db_path, path_delimiter

day_num = 6
lesson_num = 5
week_len = day_num * lesson_num


def get_teacher_list(raw=False):
    # Slice teacher list, context search
    teacher_set = set()
    with open('./db/_Teachers.txt', 'rt') as out:
        teachers = out.readlines()
        for teacher in teachers:
            if not raw:
                teach_s = teacher.decode('cp1251')[:-2].split(', ')
            else:
                teach_s = {teacher.decode('cp1251')[:-2]}
            teacher_set.update(teach_s)
    teachers_list = list(teacher_set)
    teachers_list.sort()
    return teachers_list

teacher_list = get_teacher_list()
r_teacher_list = get_teacher_list(raw=True)

group_list = [_group[:-2] for _group in open('./db/dihc.txt', 'rt').readlines()]
room_path = db_path + 'Rooms' + path_delimiter
room_list = [str(k * 100 + l) for k in range(2, 6) for l in range(1, 39)]

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


def collect_lessons(content_type, content):
    lesson_set = [[None for i in range(lesson_num)] for j in range(day_num * 2)]
    if content_type is 'teacher':
        teacher = Tools_for_db.Teacher(name=content)
        for i in range(week_len * 2):
            lesson = teacher.getInfoByTime(i)
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                lesson_type = type_dict[lesson[2]]
                groups = get_groups(lesson[3])
                my_lesson = Lesson(
                    teacher=content.encode('utf-8'),
                    lesson=less.encode('utf-8'),
                    type=lesson_type,
                    groups=groups,
                    room=str(int(room)),
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='teacher',
                    update=update_lesson
                )
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    teacher=content.encode('utf-8'),
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='empty',
                    update=update_lesson
                )

    elif content_type is 'group':
        group = Tools_for_db.Group(name=content)
        for i in range(week_len * 2):
            lesson = group.getInfoByTime(i)
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                lesson_type = type_dict[lesson[2]]
                teach = lesson[3]
                my_lesson = Lesson(
                    teacher=teach.encode('utf-8'),
                    lesson=less.encode('utf-8'),
                    type=lesson_type,
                    groups=[group.name],
                    room=str(int(room)),
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='group',
                    update=update_lesson
                )
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    groups=[group.name],
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='empty',
                    update=update_lesson
                )
    elif content_type is 'room':
        try:
            with open(room_path + 'Lec' + path_delimiter + content +
                              '.csv', 'r') as f:
                lessons = list(
                    UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
        except IOError:
            try:
                with open(room_path + 'Lab' + path_delimiter + content +
                                  '.csv', 'r') as f:
                    lessons = list(
                        UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
            except IOError:
                try:
                    with open(room_path + 'Prac' + path_delimiter + content +
                                      '.csv', 'r') as f:
                        lessons = list(
                            UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                except IOError:
                    print 'Oops..'
                    return lesson_set

        for i in range(week_len * 2):
            lesson = lessons[i][0]
            if lesson != u'0':
                stop = unicode(':', 'utf-8')

                group, less, lesson_type, teach = tuple(lesson.split(stop))
                lesson_type = type_dict[lesson_type]
                room = content
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                my_lesson = Lesson(
                    teacher=teach.encode('utf-8'),
                    lesson=less.encode('utf-8'),
                    type=lesson_type,
                    groups=get_groups(group.decode('cp1251')),
                    room=str(int(room)),
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='room',
                    update=update_lesson
                )
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='empty',
                    update=update_lesson
                )
    else:
        print 'Oops..'
    return lesson_set


def merge_schedule(first, second):
    lesson_set = [[None for i in range(lesson_num)] for j in range(day_num * 2)]
    for i in range(week_len * 2):
        first_one = first[i / lesson_num][i % lesson_num]
        second_one = second[i / lesson_num][i % lesson_num]
        if first_one == second_one:
            result = first_one
        elif first_one.empty():
            result = second_one
        elif second_one.empty():
            result = first_one
        else:
            print 'Have errors merging tables'
            return first
        lesson_set[i / lesson_num][i % lesson_num] = result
    return lesson_set


def update_lesson(old_lesson, new_lessons, temp=True):
    print 'Lesson %s updated, %s' % \
          (old_lesson.lesson, 'Temp' if temp else 'Perm')
    print 'To %s' % new_lessons[0].lesson


if __name__ == '__main__':
    pass
