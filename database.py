#!/usr/bin/python
# -*- coding: utf-8 -*-#
"""
Definitions for Easy Week database structure
"""
from random import random
from lessons import Lesson, clickable, data_lesson

week_len = 6
day_len = 5

teacher_list = []
group_list = []
room_list = []


def get_lesson_set():
    return [[Lesson(on_release=clickable,
                    **data_lesson[int(random() * 100) % 2])
            for i in range(60)] for j in range(70)]


def collect_teachers(lesson_set):
    global teacher_list
    pass


def collect_groups(lesson_set):
    global group_list
    pass


def collect_rooms(lesson_set):
    global room_list
    pass


def to_teachers(lesson_set):
    global teacher_list
    teacher_set = [[None] * len(lesson_set[0])] * len(teacher_list)
    for group in lesson_set:
        for i in range(len(group)):
            if group[i].teacher is not '':
                teacher_index = teacher_list.index(group[i].teacher)
                teacher_set[teacher_index[i]] = group[i]
    return teacher_set


def to_teacher(lesson_set, teacher):
    global teacher_list
    teacher_set = [[None] * day_len] * week_len
    for group in lesson_set:
        for i in range(len(group)):
            if group[i].teacher is not '':
                teacher_index = teacher_list.index(group[i].teacher)
                teacher_set[teacher_index[i]] = group[i]
    return teacher_set


def to_rooms(lesson_set):
    global rooms_list
    teacher_set = [[None] * len(lesson_set[0])] * len(teacher_list)
    for group in lesson_set:
        for i in range(len(group)):
            if group[i].teacher is not '':
                teacher_index = teacher_list.index(group[i].teacher)
                teacher_set[teacher_index[i]] = group[i]
    return teacher_set
