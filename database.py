#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week database structure
"""
import csv
from lessons import Lesson, lesson_click, data_lesson
from db import Tools_for_db
from db.BlakMagicAlogorithm import getTeacher, UnicodeReader
from db.Tools_for_db import db_path, path_delimiter

week_len = 6
day_len = 5
week_num = week_len * day_len

teacher_list = [teacher.decode('cp1251')[:-2] for teacher
                in open('./db/_Teachers.txt', 'rt').readlines()]

group_list = [group[:-2] for group in open('./db/dihc.txt', 'rt').readlines()]

room_path = db_path + 'Rooms' + path_delimiter
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


def collect_lessons(content_type, content):
    lesson_set = [[None for i in range(day_len)] for j in range(week_len * 2)]
    if content_type is 'teacher':
        teacher = Tools_for_db.Teacher(name=content)
        for i in range(week_num * 2):
            lesson = teacher.getInfoByTime(i)
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                type = type_dict[lesson[2]]
                groups = get_groups(lesson[3])
                my_lesson = Lesson(teacher=content.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=type,
                                   groups=groups,
                                   room=str(int(room)),
                                   week=('upper' if i < week_num else 'lower'),
                                   day=(i / day_len % week_len),
                                   number=(i % day_len))
                lesson_set[i / day_len][i % day_len] = my_lesson
            else:
                lesson_set[i / day_len][i % day_len] = Lesson(
                    teacher=content.encode('utf-8'),
                    week=('upper' if i < week_num else 'lower'),
                    day=(i / day_len % week_len),
                    number=(i % day_len)
                )

    elif content_type is 'group':
        group = Tools_for_db.Group(name=content)
        for i in range(week_num * 2):
            lesson = group.getInfoByTime(i)
            if lesson[0] is not '':
                room = lesson[0]
                less = lesson[1]
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                type = type_dict[lesson[2]]
                teach = lesson[3]
                my_lesson = Lesson(teacher=teach.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=type,
                                   groups=[group.name],
                                   room=str(int(room)),
                                   week=('upper' if i < week_num else 'lower'),
                                   day=(i / day_len % week_len),
                                   number=(i % day_len))
                lesson_set[i / day_len][i % day_len] = my_lesson
            else:
                lesson_set[i / day_len][i % day_len] = Lesson(
                    groups=[group.name],
                    week=('upper' if i < week_num else 'lower'),
                    day=(i / day_len % week_len),
                    number=(i % day_len)
                )
    elif content_type is 'room':
        try:
            with open(room_path+'Lec'+path_delimiter+str(content)+'.csv', 'r') as f:
                roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                type = type_dict[unicode('Лек', 'utf-8')]
        except IOError:
            try:
                with open(room_path+'Lab'+path_delimiter+str(content)+'.csv', 'r') as f:
                    roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                    type = type_dict[unicode('Лаб', 'utf-8')]
            except IOError:
                try:
                    with open(room_path+'Prac'+path_delimiter+str(content)+'.csv', 'r') as f:
                        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
                        type = type_dict[unicode('Прак', 'utf-8')]
                except IOError:
                    print 'Oops..'
                    return None
        
        for i in range(60):
            lesson = roomList[i]
            if lesson[0] is not '0':
                word = ''
                data_number = 0
                stop = unicode(':', 'utf-8')
                for let in lesson[0]:
                    if let != stop:
                        word += let
                    else:
                        if data_number is 0:
                            group = word
                        elif data_number is 1:
                            less = word
                        elif data_number is 2:
                            pass
                        else:
                            pass

                        data_number += 1
                        word = ''

                teach = word
                room = str(content)
                # 'Лек' -> 'lect, 'Лаб' -> 'lab, 'Прак' -> 'pract'
                my_lesson = Lesson(teacher=teach.encode('utf-8'),
                                   lesson=less.encode('utf-8'),
                                   type=type,
                                   groups=get_groups(group.decode('cp1251')),
                                   room=str(int(room)),
                                   week=('upper' if i < week_num else 'lower'),
                                   day=(i / day_len % week_len),
                                   number=(i % day_len))
                lesson_set[i / day_len][i % day_len] = my_lesson
            else:
                lesson_set[i / day_len][i % day_len] = Lesson(
                    week=('upper' if i < week_num else 'lower'),
                    day=(i / day_len % week_len),
                    number=(i % day_len)
                )
    else:
        print 'Oops..'
    return lesson_set


if __name__ == '__main__':
    less = collect_lessons('room', content=507)