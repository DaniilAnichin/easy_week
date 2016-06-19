#!/usr/bin/python
# -*- coding: utf-8 -*-#

import csv
import codecs
import cStringIO
import os
import lessons

typeDict = {unicode('Лек', 'utf-8'): 'Lec',  unicode('Лаб', 'utf-8'): 'Lab',
            unicode('Прак', 'utf-8'): 'Pract'}


# db_path = "D:\KPI\Kursach\Db\\"
# path_delimiter = '\\'
db_path = '/home/anichindaniil/Python/projects/easy_week/db/'
path_delimiter = '/'


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwargs):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
        

class Group:
    name = ''
    path = ''
    dataList = []

    def __init__(self, name):
        self.name = name
        self.path = db_path
        try:
            f = open(
                self.path + 'Groups' + path_delimiter + name + '.csv',
                'rb'
            )
            self.dataList = list(
                UnicodeReader(f, csv.excel, 'cp1251', delimiter=';')
            )
            f.close()
        except IOError:
            pass
            #print "None such group : {0}".format(name)
            
    def addLesson(self, lesName, lesType, room, time, temp):
        adding_path = 'Tmp' + path_delimiter if temp else ''
        if lesType == u'':
            for row in self.dataList[1:]:
                if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1]) ):                      #u'\u003a' = ':'
                    if row[3].count(unicode(':', 'utf-8')) < int(row[2]):
                        row[3] = row[3]+str(time)+','+str(room)+':'                
                fg = open(
                    self.path + 'Groups' + path_delimiter + self.name + '.csv',
                    'wb'
                )
                fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                fgWriter.writerows(self.dataList)
                fg.close()
                return 0
            return -1
        
        try:
            f = open(
                self.path + 'Rooms' + path_delimiter + typeDict[lesType] +
                path_delimiter + str(room) + '.csv',
                'rb'
            )
            nonUniLesType = typeDict[lesType]
        except IOError:
            print '1'
            return -1

        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))

        f.close()
        if cmp(roomList[time][0], str(0)):
            print 'room busy'
            return 'room busy'
        if not str(room) in self.dataList[0][0]:
            print '3 - wrong group room'
        if cmp(self.getInfoByTime(time)[0], ''):
            print 'group busy'
            return 'group busy'
        
        #lesName = unicode(lesName, 'utf-8')
        #lesType = unicode(lesType, 'utf-8')
        for row in self.dataList[1:]:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):                      #u'\u003a' = ':'
                if row[3].count(unicode(':', 'utf-8')) < int(row[2]):
                    teacher = Teacher(row[0][row[0].index(u'\u003a')+1:])
                    if cmp(lesType, unicode('Лек', 'utf-8')):
                        for trow in teacher.dataList:
                            if not (cmp(lesName, trow[0][:trow[0].index(u'\u003a')]) or cmp(lesType, trow[1]) or cmp(self.name, trow[0][trow[0].index(u'\u003a')+1:])):
                                print "We are so deep, near the bottom"
                                if teacher.getInfoByTime(time)[0] != u'':
                                    print 'teacher busy'
                                    return 'teacher busy'
                                trow[3] = trow[3]+str(time)+','+str(room)+':'
                                row[3] = row[3]+str(time)+','+str(room)+':'
                                roomList[time][0] = self.name+':'+lesName+':'+lesType+':'+row[0][row[0].index(':')+1:]
                                try:
                                    ft = open(
                                        self.path+adding_path+'Teach' +
                                        path_delimiter+teacher.name+'.csv',
                                        'wb'
                                    )
                                    print teacher.name.encode('cp1251')
                                    fg = open(
                                        self.path+adding_path+'Groups'+
                                        path_delimiter+self.name+'.csv', 'wb'
                                    )
                                    fr = open(
                                        self.path+adding_path+'Rooms'+
                                        path_delimiter+nonUniLesType+
                                        path_delimiter+str(room)+'.csv', 'wb'
                                    )
                                except IOError:
                                    print "Why, tell me why"
                                    return -1
                                ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
                                fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                                frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter=';')
                                ftWriter.writerows(teacher.dataList)
                                fgWriter.writerows(self.dataList)
                                frWriter.writerows(roomList)
                                ft.close()
                                fg.close()
                                fr.close()
                                return 0
                    else:
                        stream = []
                        for i in range(6):
                            if i+1 != int(self.name[-1]):
                                stream.append(Group(self.name[:-1]+str(i+1)))
                                if not cmp(stream[i-1].dataList, []):
                                    del stream[-1]
                                    break
                        for les in stream:
                            if les.getInfoByTime(time)[0] is not '':
                                return -1
                        for trow in teacher.dataList:
                            if not (cmp(lesName, trow[0][:trow[0].index(u'\u003a')]) or cmp(lesType, trow[1]) or cmp(self.name[:-1], trow[0][trow[0].index(u'\u003a')+1:])):
                                print "We are so deep, near the bottom"
                                row[3] = row[3]+str(time)+','+str(room)+':'
                                for group in stream:
                                    for line in group.dataList[1:]:
                                        if not (cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1])):
                                            line[3] = line[3]+str(time)+','+str(room)+':'
                                trow[3] = trow[3]+str(time)+','+str(room)+':'
                                roomList[time][0] = self.name[:-1]+':'+lesName+':'+lesType+':'+row[0][row[0].index(':')+1:]
                                try:
                                    ft = open(self.path+adding_path+'Teach'+path_delimiter+row[0][row[0].index(':')+1:]+'.csv', 'wb')
                                    fg = open(self.path+adding_path+'Groups'+path_delimiter+self.name+'.csv', 'wb')
                                    fr = open(self.path+adding_path+'Rooms'+path_delimiter+nonUniLesType+path_delimiter+str(room)+'.csv', 'wb')
                                except IOError:
                                    print "Why, tell me why"
                                    return -1
                                ftWriter = UnicodeWriter(
                                    ft, csv.excel, 'cp1251', delimiter=';'
                                )
                                fgWriter = UnicodeWriter(
                                    fg, csv.excel, 'cp1251', delimiter=';'
                                )
                                frWriter = UnicodeWriter(
                                    fr, csv.excel, 'cp1251', delimiter=';'
                                )
                                ftWriter.writerows(teacher.dataList)
                                fgWriter.writerows(self.dataList)
                                frWriter.writerows(roomList)
                                ft.close()
                                fg.close()
                                fr.close()
                                for group in stream:
                                    fg = open(self.path+'Groups'+path_delimiter+group.name+'.csv', 'wb')
                                    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                                    fgWriter.writerows(group.dataList)
                                    fg.close()
                                return 0
                    
            else:
                continue
    
    def getInfoByTime(self, time):
        for row in self.dataList[1:]:
            a = row[3].count(':')
            if a == 0:
                continue
            ftime = ''
            for let in row[3]:
                if cmp(let, ':'):
                    ftime += let
                elif int(ftime[:ftime.index(',')]) == time:
                    return [ftime[ftime.index(',')+1:], row[0][:row[0].index(u'\u003a')], row[1], row[0][row[0].index(u'\u003a')+1:]]
                else:
                    ftime = ''
        return['', '', '', '']

    def getTimeByLesson(self, lesName, lesType):
        lesName = unicode(lesName, 'utf-8')
        lesType = unicode(lesType, 'utf-8')
        for row in self.dataList[1:]:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):
                times = []
                a = row[3].count(':')
                retrow = ''
                if a == 0:
                    return ['']
                for let in row[3]:
                    if cmp(let, ':'):
                        retrow += let
                    else:
                        times.append(retrow)
                        retrow=''
                return times

    def removeLessonByTime(self, time, temp):
        adding_path = 'Tmp' + path_delimiter if temp else ''
        info = self.getInfoByTime(time)
        if info[0] != u'':
            teacher = Teacher(info[3])
            try:
                f = open(self.path+'Rooms'+path_delimiter+typeDict[info[2]]+path_delimiter+info[0]+'.csv', 'rb')
                nonUniLesType = typeDict[info[2]]
            except IOError:
                print '1'
                print nonUniLesType
                return -1
            roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter = ';'))
            f.close()
            for row in self.dataList[1:]:
                if not ( cmp(info[1], row[0][:row[0].index(u'\u003a')]) or cmp(info[2], row[1]) ):
                    ftime = ''
                    for let in row[3]:
                        if cmp(let, ':'):
                            ftime += let
                        elif int(ftime[:ftime.index(',')]) == time:
                            row[3] = row[3].replace(str(ftime)+u'\u003a', '')
                            break
                        else:
                            ftime = ''
            for row in teacher.dataList:
                if not ( cmp(info[1], row[0][:row[0].index(u'\u003a')]) or cmp(info[2], row[1]) ):
                    ftime = ''
                    for let in row[3]:
                        if cmp(let, ':'):
                            ftime += let
                        elif int(ftime[:ftime.index(',')]) == time:
                            row[3] = row[3].replace(str(ftime)+u'\u003a', '')
                            break
                        else:
                            ftime = ''
            roomList[time] = '0'
            try:
                #print teacher.name.encode('cp1251')
                ft = open(self.path+adding_path+'Teach'+path_delimiter+teacher.name+'.csv', 'wb')
                fg = open(self.path+adding_path+'Groups'+path_delimiter+self.name+'.csv', 'wb')
                fr = open(self.path+adding_path+'Rooms'+path_delimiter+nonUniLesType+path_delimiter+info[0]+'.csv', 'wb')
            except IOError:
                print "Why, tell me why"
                return -1
            ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
            fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
            frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter=';')
            ftWriter.writerows(teacher.dataList)
            fgWriter.writerows(self.dataList)
            frWriter.writerows(roomList)
            ft.close()
            fg.close()
            fr.close()
            return 0
        else:
            return -1


class Teacher:
    dataList = []
    name = ''
    path = ''
    
    def __init__(self, name):
        self.name = name
        self.path = db_path
        try:
            f = open(self.path+'Teach'+path_delimiter+name+'.csv', 'rb')
            self.dataList = list(
                UnicodeReader(f, csv.excel, 'cp1251', delimiter=';')
            )
            f.close()
        except IOError:
            print "None such teacher :{0}".format(name.encode('cp1251'))
        
    def addLesson(self, lesName, lesType, room, time, groupName='', temp=False):
        adding_path = 'Tmp' + path_delimiter if temp else ''
        try:
            f = open(self.path+'Rooms'+path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'rb')
            #nonUniLesType = typeDict[lesType]
        except IOError:
            print '1'
            print typeDict[lesType]
            print str(room)
            print time
            return -1
        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
        f.close()
        if cmp(roomList[time][0], str(0)):
            print '2'
            print time
            print roomList[time][0].encode('cp1251')
            print room
            return -1        
        #lesName = unicode(lesName, 'utf-8')
        #lesType = unicode(lesType, 'utf-8')
        if cmp(self.getInfoByTime(time)[0], ''):
            return -1
        if not cmp(lesType, unicode('Лек', 'utf-8')):
            stream = []
            for row in self.dataList:
                if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):
                    for i in range(6):
                        stream.append(Group(row[0][row[0].index(u'\u003a')+1:]+str(i+1)))
                        if not cmp(stream[i].dataList, []):
                            del stream[-1]
                            break
                else:
                    continue
                for les in stream:
                    if cmp(les.getInfoByTime(time)[0], ''):
                        return -1
                if not str(room) in stream[0].dataList[0][0]:
                    #print 'yo'
                    return -1
                if not int(row[2]) > row[3].count(u'\u003a'):
                    #print 'yoyo'
                    return -1
                row[3] = row[3]+str(time)+','+str(room)+':'
                for group in stream:
                    for line in group.dataList[1:]:
                         if not (cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1])):
                            line[3] = line[3]+str(time)+','+str(room)+':'
                roomList[time][0] = stream[0].name[:-1]+':'+lesName+':'+lesType+':'+self.name
                try:
                    ft = open(self.path+adding_path+'Teach'+path_delimiter+self.name+'.csv', 'wb')
                    fr = open(self.path+adding_path+'Rooms'+path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'wb')
                except IOError:
                    print "Why, tell me why"
                    return -1
                ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
                frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter=';')
                ftWriter.writerows(self.dataList)
                frWriter.writerows(roomList)
                ft.close()
                fr.close()
                for group in stream:
                    fg = open(self.path+adding_path+'Groups'+path_delimiter+group.name+'.csv', 'wb')
                    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                    fgWriter.writerows(group.dataList)
                    fg.close()
                return 0
        else:
            #group = Group
            for row in self.dataList:
                if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1]) or cmp(row[0][row[0].index(u'\u003a')+1:], groupName)):
                    group = Group(groupName)
                else:
                    continue
                if cmp(group.getInfoByTime(time)[0], ''):
                    return -1
                if not str(room) in group.dataList[0][0]:
                    return -1
                if not int(row[2]) > row[3].count(u'\u003a'):
                    return -1
                row[3] = row[3]+str(time)+','+str(room)+':'
                for line in group.dataList[1:]:
                    if not (cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1])):
                        line[3] = line[3]+str(time)+','+str(room)+':'
                roomList[time][0] = group.name+':'+lesName+':'+lesType+':'+self.name
                try:
                    ft = open(self.path+adding_path+'Teach'+path_delimiter+self.name+'.csv', 'wb')
                    fg = open(self.path+adding_path+'Groups'+path_delimiter+group.name+'.csv', 'wb')
                    fr = open(self.path+adding_path+'Rooms'+path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'wb')
                except IOError:
                    print "Why, tell me why"
                    return -1
                ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
                fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter=';')
                ftWriter.writerows(self.dataList)
                fgWriter.writerows(group.dataList)
                frWriter.writerows(roomList)
                ft.close()
                fg.close()
                fr.close()
                return 0

    def getInfoByTime(self, time):
        for row in self.dataList:
            a = row[3].count(':')
            if a == 0:
                continue
            ftime = ''
            for let in row[3]:
                if cmp(let, ':'):
                    ftime += let
                elif int(ftime[:ftime.index(',')]) == time:
                    return [ftime[ftime.index(',')+1:], row[0][:row[0].index(u'\u003a')], row[1], row[0][row[0].index(u'\u003a')+1:]]
                else:
                    ftime = ''
        return['', '', '', '']
        
    def getTimeByLesson(self, lesName, lesType):    
        lesName = unicode(lesName, 'utf-8')
        lesType = unicode(lesType, 'utf-8')
        for row in self.dataList[1:]:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):
                times = []
                a = row[3].count(':')
                retrow = ''
                if a == 0:
                    return ['']
                for let in row[3]:
                    if cmp(let, ':'):
                        retrow += let
                    else:
                        times.append(retrow)
                        retrow=''
                return times


def addNewLessonForGroupAndTeacher(group, teacher, count, lessonName, type):
    group.dataList.append(lessonName+u'\u003a'+teacher, type, str(count), '')
    if type is unicode('Лек', 'utf-8'):
        teacher.dataList.append(lessonName+u'\u003a'+group[:-1], type, str(count), '')
    else:
        teacher.dataList.append(lessonName+u'\u003a'+group, type, str(count), '')
    temp = group.dataList[0]
    group.dataList = sorted(group.dataList[1:], key=lambda lrow:lrow[2], reverse=True)
    group.dataList.insert(0, temp)
    teacher.dataList = sorted(teacher.dataList[1:], key=lambda lrow:lrow[2], reverse=True)
    try:
        ft = open(teacher.path+'Teach'+path_delimiter+teacher.name+'.csv', 'wb')
        fg = open(teacher.path+'Groups'+path_delimiter+group.name+'.csv', 'wb')
    except IOError:
        print "Why, tell me why"
        return -1
    ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
    ftWriter.writerows(teacher.dataList)
    fgWriter.writerows(group.dataList)
    ft.close()
    fg.close()
    return 0


def deleteLessonForGroupAndTeacher(group, teacher, count, lesName, lesType):
    for row in group.dataList[1:]:
        if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):
            del group.dataList[row]
            break
        
    if type is unicode('Лек', 'utf-8'):
        for row in teacher.dataList:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):
                del teacher.dataList[row]
                break    
    else:
        for row in teacher.dataList:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1]) or cmp(group.name, row[0][row[0].index(u'\u003a')+1:])):
                del teacher.dataList[row]
                break
    try:
        ft = open(teacher.path+'Teach'+path_delimiter+teacher.name+'.csv', 'wb')
        fg = open(teacher.path+'Groups'+path_delimiter+group.name+'.csv', 'wb')
    except IOError:
        print "Why, tell me why"
        return -1
    ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
    ftWriter.writerows(teacher.dataList)
    fgWriter.writerows(group.dataList)
    ft.close()
    fg.close()
    return 0                
        
#teaceher =Teacher(unicode("ас. Габинет А. В.", 'utf-8'))
#teaceher.addLesson(teaceher.dataList[2][0][:teaceher.dataList[2][0].index(u'\u003a')], teaceher.dataList[2][1], 510, 8, 'ip-32')
#group = Group('io-21')
#for i in range(60):
#    group.removeLessonByTime(i)


