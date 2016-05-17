#!/usr/bin/python
# -*- coding: utf-8 -*-#
from Tools_for_db import *
import csv, codecs, cStringIO
import random

random.seed()
#typeDict = {'Лек' : 'Lec', 'Лаб':'Lab', 'Прак':'Pract'}
teachers = codecs.open('D:\KPI\Kursach\Db\_Teachers.txt', 'r', 'cp1251')

def getTeacher(pos):
    teachers.seek(0)
    for i in range(pos):
        try:
            teachers.readline()
        except IOError:
            return -1
    return unicode(teachers.readline()[:-1])[:-1]

seq = range(194)
random.shuffle(seq)
for i in seq:
    teacher = Teacher(getTeacher(i))
    for line in teacher.dataList:
        if not cmp(line[1], unicode('Лек', 'utf-8')):
            group = Group(line[0][line[0].index(u'\u003a')+1:]+str(1))
            roomSeq = []
            num = ''
            for n in group.dataList[0][0]:
                if cmp(n, ','):
                    num+=n
                else:
                    if int(num[1:])>28:
                        roomSeq.append(int(num))
                    num = ''
            random.shuffle(roomSeq)
            for i in range(int(line[2])):
                breakItterator = 0
                addingFlag = 0
                print 'New les'
                while not addingFlag:
                    addingFlag = 0
                    breakItterator += 1
                    if breakItterator>100:
                        addingFlag = 1
                        break
                    random.shuffle(roomSeq)
                    j = random.choice(roomSeq)
                    day = int((random.randint(0,6000000)%60)/5)
                    while day==5 and day==11:
                        day = int((random.randint(0,6000000)%60)/5)
                    newDayFlag = 1
                    contLes = 0
                    for chekLes in range(4):
                        if cmp('', teacher.getInfoByTime(day*5+chekLes)[0]):
                            newDayFlag = 0
                            contLes = chekLes
                            break
                        if cmp('', group.getInfoByTime(day*5+chekLes)[0]):
                            newDayFlag = 0
                            contLes = chekLes
                            break
                    if newDayFlag:
                        lesNum = random.randint(0,1)
                        for room in roomSeq:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, day*5+lesNum)
                            if not res:
                                addingFlag =1
                                break
                    elif chekLes<3:
                        for room in roomSeq:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, day*5+chekLes+1)
                            if not res:
                                addingFlag =1
                                break
                    time = random.randint(0,1000000)%60
                    while not time%5==4 and not int(time/5)==5 and not int(time/5)==11:
                        time = random.randint(0,1000000)%60
                    if (time%5 == 0 or time%5 == 1):
                        for room in roomSeq:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, time) 
                            if not res:
                                addingFlag =1
                                break
                    else:
                        if not(cmp(group.getInfoByTime(time-1)[0], '') and cmp(teacher.getInfoByTime(time-1)[0], '')):
                            continue
                        else:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], j, time)
                    if not res: 
                        addingFlag = 1
random.shuffle(seq)
for i in seq:
    teacher = Teacher(getTeacher(i))
    for line in teacher.dataList:
        if cmp(line[1], unicode('Лек', 'utf-8')):
            group = Group(line[0][line[0].index(u'\u003a')+1:])
            roomSeq = []
            num = ''
            for n in group.dataList[0][0]:
                if cmp(n, ','):
                    num+=n
                else:
                    if not cmp(line[1], unicode('Лаб', 'utf-8')):
                        if int(num[1:])<17:
                            roomSeq.append(int(num))
                        num = ''
                    else:
                        if int(num[1:])>=17 and int(num[1:])<=28:
                            roomSeq.append(int(num))
                        num = ''
            random.shuffle(roomSeq)
            for i in range(int(line[2])):
                breakItterator = 0
                addingFlag = 0
                print 'New les'
                while not addingFlag:
                    addingFlag = 0
                    breakItterator += 1
                    if breakItterator>100:
                        addingFlag = 1
                        break
                    print roomSeq
                    random.shuffle(roomSeq)
                    j = random.choice(roomSeq)
                    day = int((random.randint(0,6000000)%60)/5)
                    while day==5 and day==11:
                        day = int((random.randint(0,6000000)%60)/5)
                    newDayFlag = 1
                    contLes = 0
                    for chekLes in range(4):
                        if cmp('', teacher.getInfoByTime(day*5+chekLes)[0]):
                            newDayFlag = 0
                            contLes = chekLes
                            break
                        if cmp('', group.getInfoByTime(day*5+chekLes)[0]):
                            newDayFlag = 0
                            contLes = chekLes
                            break
                    if newDayFlag:
                        lesNum = random.randint(0,1)
                        for room in roomSeq:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, day*5+lesNum)
                            if not res:
                                addingFlag =1
                                break
                    elif chekLes<3:
                        for room in roomSeq:
                            res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, day*5+chekLes+1)
                            if not res:
                                addingFlag =1
                                break
                    # time = random.randint(0,1000000)%60
                    # while time%5==4 and int(time/5)==5 and int(time/5)==11:
                        # time = random.randint(0,1000000)%60
                    # if (time%5 == 0 or time%5 == 1):
                        # for room in roomSeq:
                            # res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], room, time) 
                            # if not res:
                                # addingFlag =1
                                # break
                    # else:
                        # if not(cmp(group.getInfoByTime(time-1)[0], '') and cmp(teacher.getInfoByTime(time-1)[0], '')):
                            # continue
                        # else:
                            # res = teacher.addLesson(line[0][:line[0].index(u'\u003a')], line[1], j, time)
                    # if not res: 
                        # addingFlag = 1