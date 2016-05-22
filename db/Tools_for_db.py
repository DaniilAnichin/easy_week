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

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
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
            f=open(self.path+"Groups\\"+name+".csv", 'rb')
            self.dataList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
            f.close()
        except IOError:
            pass
            #print "None such group : {0}".format(name)

    def addLesson(self, lesName, lesType, room, time):
        try:
            f = open(self.path+'Rooms' + path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'rb')
            nonUniLesType = typeDict[lesType]
        except IOError:
            print '1'
            print nonUniLesType
            return -1
        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter=';'))
        f.close()
        if cmp(roomList[time][0], str(0)):
            print '2'
            return -1
        if not str(room) in self.dataList[0][0]:
            print '3'
            return -1
        if cmp(self.getInfoByTime(time)[0], ''):
            return -1

        lesName = unicode(lesName, 'utf-8')
        lesType = unicode(lesType, 'utf-8')
        for row in self.dataList[1:]:
            if not (cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1])):          #u'\u003a' = ':'
                print 'Hi'
                if row[3].count(unicode(':', 'utf-8')) < int(row[2]):
                    teacher = Teacher(row[0][row[0].index(u'\u003a')+1:])
                    if cmp(lesType, unicode('Лек', 'utf-8')):
                        for trow in teacher.dataList:
                            if not (cmp(lesName, trow[0][:trow[0].index(u'\u003a')]) or cmp(lesType, trow[1]) or cmp(self.name, trow[0][trow[0].index(u'\u003a')+1:])):
                                print "We are so deep, near the bottom"
                                row[3] = row[3]+str(time)+','+str(room)+':'
                                trow[3] = trow[3]+str(time)+','+str(room)+':'
                                roomList[time][0] = self.name+':'+lesName+':'+lesType+':'+row[0][row[0].index(':')+1:]
                                try:
                                    ft = open(self.path+'Teach' + path_delimiter+teacher.name+'.csv', 'wb')
                                    print teacher.name.encode('cp1251')
                                    fg = open(self.path+'Groups' + path_delimiter+self.name+'.csv', 'wb')
                                    fr = open(self.path+'Rooms' + path_delimiter+nonUniLesType+path_delimiter+str(room)+'.csv', 'wb')
                                except IOError:
                                    print "Why, tell me why"
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
                            if cmp(les.getInfoByTime(time)[0], ''):
                                return -1
                        for trow in teacher.dataList:
                            if not ( cmp(lesName, trow[0][:trow[0].index(u'\u003a')]) or cmp(lesType, trow[1]) or cmp(self.name[:-1], trow[0][trow[0].index(u'\u003a')+1:] )):
                                print "We are so deep, near the bottom"
                                row[3] = row[3]+str(time)+','+str(room)+':'
                                for group in stream:
                                    for line in group.dataList[1:]:
                                         if not ( cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1]) ):
                                            line[3] = line[3]+str(time)+','+str(room)+':'
                                trow[3] = trow[3]+str(time)+','+str(room)+':'
                                roomList[time][0] = self.name[:-1]+':'+lesName+':'+lesType+':'+row[0][row[0].index(':')+1:]
                                try:
                                    ft = open(self.path+'Teach' + path_delimiter+row[0][row[0].index(':')+1:]+'.csv', 'wb')
                                    fg = open(self.path+'Groups' + path_delimiter+self.name+'.csv', 'wb')
                                    fr = open(self.path+'Rooms' + path_delimiter+nonUniLesType+path_delimiter+str(room)+'.csv', 'wb')
                                except IOError:
                                    print "Why, tell me why"
                                ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter=';')
                                fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                                frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter=';')
                                ftWriter.writerows(teacher.dataList)
                                fgWriter.writerows(self.dataList)
                                frWriter.writerows(roomList)
                                ft.close()
                                fg.close()
                                fr.close()
                                for group in stream:
                                    fg = open(self.path+'Groups' + path_delimiter+group.name+'.csv', 'wb')
                                    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter=';')
                                    fgWriter.writerows(group.dataList)
                                    fg.close()
                                return 0

                else:
                    print '5'
                    return -1
                break

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


class Teacher:
    dataList = []
    name = ''
    path = ''

    def __init__(self, name):
        self.name = name
        self.path = db_path
        try:
            f = open(self.path+'Teach' + path_delimiter+self.name+'.csv', 'rb')
            # f = open('%sTeach%s%s.csv' % (self.path, path_delimiter, self.name), 'rb')
            self.dataList = list(UnicodeReader(f, csv.excel, 'cp1251',
                                               delimiter=';'))
            f.close()
        except IOError:
            print "None such teacher : {0}".format(self.name.encode('cp1251'))

    def addLesson(self, lesName, lesType, room, time):
        try:
            f = open(self.path+'Rooms' + path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'rb')
            #nonUniLesType = typeDict[lesType]
        except IOError:
            print '1'
            print typeDict[lesType]
            print str(room)
            print time
            return -1
        roomList = list(UnicodeReader(f, csv.excel, 'cp1251', delimiter = ';'))
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
        if  not cmp(lesType, unicode('Лек', 'utf-8')):
            stream = []
            for row in self.dataList:
                if not ( cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1]) ):
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
                if not int(row[2])>row[3].count(u'\u003a'):
                    #print 'yoyo'
                    return -1
                row[3] = row[3]+str(time)+','+str(room)+':'
                for group in stream:
                    for line in group.dataList[1:]:
                         if not ( cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1]) ):
                            line[3] = line[3]+str(time)+','+str(room)+':'
                roomList[time][0] = stream[0].name[:-1]+':'+lesName+':'+lesType+':'+self.name
                try:
                    ft = open(self.path+'Teach' + path_delimiter+self.name+'.csv', 'wb')
                    fr = open(self.path+'Rooms' + path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'wb')
                except IOError:
                    print "Why, tell me why"
                ftWriter = UnicodeWriter(ft, csv.excel, 'cp1251', delimiter = ';')
                frWriter = UnicodeWriter(fr, csv.excel, 'cp1251', delimiter = ';')
                ftWriter.writerows(self.dataList)
                frWriter.writerows(roomList)
                ft.close()
                fr.close()
                for group in stream:
                    fg = open(self.path+'Groups' + path_delimiter+group.name+'.csv', 'wb')
                    fgWriter = UnicodeWriter(fg, csv.excel, 'cp1251', delimiter = ';')
                    fgWriter.writerows(group.dataList)
                    fg.close()
                return 0
        else:
            #group = Group
            for row in self.dataList:
                if not ( cmp(lesName, row[0][:row[0].index(u'\u003a')]) or cmp(lesType, row[1]) ):
                    group = Group(row[0][row[0].index(u'\u003a')+1:])
                else:
                    continue
                if cmp(group.getInfoByTime(time)[0], ''):
                    return -1
                if not str(room) in group.dataList[0][0]:
                    return -1
                if not int(row[2])>row[3].count(u'\u003a'):
                    return -1
                row[3] = row[3]+str(time)+','+str(room)+':'
                for line in group.dataList[1:]:
                    if not ( cmp(lesName, line[0][:line[0].index(u'\u003a')]) or cmp(lesType, line[1]) ):
                        line[3] = line[3]+str(time)+','+str(room)+':'
                roomList[time][0] = group.name+':'+lesName+':'+lesType+':'+self.name
                try:
                    ft = open(self.path+'Teach' + path_delimiter+self.name+'.csv', 'wb')
                    fg = open(self.path+'Groups' + path_delimiter+group.name+'.csv', 'wb')
                    fr = open(self.path+'Rooms' + path_delimiter+typeDict[lesType]+path_delimiter+str(room)+'.csv', 'wb')
                except IOError:
                    print "Why, tell me why"
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
                        retrow = ''
                return times