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

teacher_list = [teacher.decode('cp1251')[:-2] for teacher
                in open('./db/_Teachers.txt', 'rt').readlines()]

group_list = [group[:-2] for group in open('./db/dihc.txt', 'rt').readlines()]

room_path = db_path + 'Rooms' + path_delimiter
room_list = [i*100 + j for i in range(2, 6) for j in range(1, 39)]


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
                my_lesson = Lesson(teacher=content.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=lesson_type,
                                   groups=groups,
                                   room=str(int(room)),
                                   week=('upper' if i < week_len else 'lower'),
                                   day=(i / lesson_num % day_num),
                                   number=(i % lesson_num),
                                   view_type='teacher')
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    teacher=content.encode('utf-8'),
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='teacher'
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
                my_lesson = Lesson(teacher=teach.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=lesson_type,
                                   groups=[group.name],
                                   room=str(int(room)),
                                   week=('upper' if i < week_len else 'lower'),
                                   day=(i / lesson_num % day_num),
                                   number=(i % lesson_num),
                                   view_type='group')
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    groups=[group.name],
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='group'
                )
    elif content_type is 'room':
        try:
            with open(room_path+'Lec'+path_delimiter+str(content)+'.csv', 'r') as f:
                roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                # type = type_dict[unicode('Лек', 'utf-8')]
        except IOError:
            try:
                with open(room_path+'Lab'+path_delimiter+str(content)+'.csv', 'r') as f:
                    roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                    # type = type_dict[unicode('Лаб', 'utf-8')]
            except IOError:
                try:
                    with open(room_path+'Prac'+path_delimiter+str(content)+'.csv', 'r') as f:
                        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                        # type = type_dict[unicode('Прак', 'utf-8')]
                except IOError:
                    print 'Oops..'
                    return lesson_set
        
        for i in range(60):
            lesson = roomList[i][0]
            if lesson != u'0':
                stop = unicode(':', 'utf-8')
                # word = ''
                # data_number = 0
                # for let in lesson:
                #     if let != stop:
                #         word += let
                #     else:
                #         if data_number is 0:
                #             group = word
                #         elif data_number is 1:
                #             less = word
                #         else:
                #             pass
                #
                #         data_number += 1
                #         word = ''

                group, less, lesson_type, teach = tuple(lesson.split(stop))
                lesson_type = type_dict[lesson_type]
                room = str(content)
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                my_lesson = Lesson(teacher=teach.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=lesson_type,
                                   groups=get_groups(group.decode('cp1251')),
                                   room=str(int(room)),
                                   week=('upper' if i < week_len else 'lower'),
                                   day=(i / lesson_num % day_num),
                                   number=(i % lesson_num),
                                   view_type='room')
                lesson_set[i / lesson_num][i % lesson_num] = my_lesson
            else:
                lesson_set[i / lesson_num][i % lesson_num] = Lesson(
                    week=('upper' if i < week_len else 'lower'),
                    day=(i / lesson_num % day_num),
                    number=(i % lesson_num),
                    view_type='room'
                )
    else:
        print 'Oops..'
    return lesson_set


if __name__ == '__main__':
    less = collect_lessons('room', content=507)
    print room_list
