import csv, codecs, cStringIO, os

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
    
def addinfo(tmprow, teachName):
    if not (cmp(tmprow[2], teachName)):
        flag = 0 
        teachw.seek(0)
        #prepos = 0
        linecounter = 0
        steachReader = []
        teachr.seek(0)
        for row in teachReader:
            steachReader.append(row)
        for row in steachReader:
            #prepos = f.tell()
            #print row
            if not(( cmp(tmprow[3],row[1]) or cmp(row[0], tmprow[1]+':'+tmprow[0]) )and( cmp(row[0], tmprow[1]+':'+tmprow[0][:-1]) or cmp(int(tmprow[0][-1]), 1) or  cmp(u'\u041b\u0435\u043a', tmprow[3]) )):
                row[2] = str(int(row[2])+1)
                steachReader = sorted(steachReader,key = lambda lrow:lrow[2], reverse= True)
                deleteContent(teachw)
                #print row[0]
                teachWriter.writerows(steachReader)
                teachw.flush()
                #print row[0].encode('cp1251')+row[2].encode('cp1251')
                flag = 1
                break
            else:
                linecounter+=1
        if not cmp(u'\u041b\u0435\u043a', tmprow[3]) and cmp(int(tmprow[0][-1]), 1):
            flag=1
        if not flag:
            teachw.seek(0,2)
            if not cmp(u'\u041b\u0435\u043a', tmprow[3]):
                    teachWriter.writerow([tmprow[1]+':'+tmprow[0][:-1], tmprow[3], str(1), ''])
            else:
                teachWriter.writerow([tmprow[1]+':'+tmprow[0], tmprow[3], str(1), ''])
            teachw.flush()
        return ['', '', '', ''] 
    else:
        #nextGroupTmpRow = tmprow
        return tmprow
    

fullDb = open("D:\KPI\kursach\DbPrototype1.csv", 'rb')
fullDbReaderL = list(UnicodeReader(fullDb, csv.excel, 'cp1251', delimiter = ';'))
fullDbReaderL.sort(key = lambda lrow : lrow[2])
sortedForTeahDb = open('D:\KPI\kursach\DbPrototype2.csv', 'w+b')
reriter = UnicodeWriter(sortedForTeahDb, csv.excel, 'cp1251', delimiter = ';')
reriter.writerows(fullDbReaderL)
sortedForTeahDb.seek(0)
fullDbReader = UnicodeReader(sortedForTeahDb, csv.excel, 'cp1251', delimiter = ';')
teachers = codecs.open('D:\KPI\Kursach\Db\Teachers.txt', 'w', 'cp1251')
i=0

while fullDbReader:
    if not i:
        first_row = fullDbReader.next()
        while not cmp(first_row[2], ''):
            first_row = fullDbReader.next()
    else:
        first_row = otherrow
    teachw = open('D:\KPI\Kursach\Db\Teach\\'+first_row[2]+'.csv', 'wb')
    teachr = open('D:\KPI\Kursach\Db\Teach\\'+first_row[2]+'.csv', 'rb')
    teachers.write(first_row[2])
    teachers.write('\r\n')
    teachers.flush()
    teachWriter = UnicodeWriter(teachw, csv.excel, 'cp1251', delimiter =';')
    teachReader = UnicodeReader(teachr, csv.excel, 'cp1251', delimiter = ';')
    
    otherrow = addinfo(first_row, first_row[2])
    try:
        while not cmp(otherrow[0], ""): #addinfo(fullDbReader.next(), first_row[2])
            otherrow = addinfo(fullDbReader.next(), first_row[2])
            i=1
    except StopIteration:
        teachw.close()
        teachr.close()
        break
    teachw.close()
    teachr.close()
teachers.close()
fullDb.close()
sortedForTeahDb.close()
os.remove('D:\KPI\kursach\DbPrototype2.csv')