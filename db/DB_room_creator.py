import csv, codecs, fileinput, cStringIO

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

# class UTF8Recoder:
    # """
    # Iterator that reads an encoded stream and reencodes the input to UTF-8
    # """
    # def __init__(self, f, encoding):
        # self.reader = codecs.getreader(encoding)(f)

    # def __iter__(self):
        # return self

    # def next(self):
        # return self.reader.next().encode("utf-8")

# class UnicodeReader:
    # """
    # A CSV reader which will iterate over lines in the CSV file "f",
    # which is encoded in the given encoding.
    # """

    # def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # f = UTF8Recoder(f, encoding)
        # self.reader = csv.reader(f, dialect=dialect, **kwds)

    # def next(self):
        # row = self.reader.next()
        # return [unicode(s, "utf-8") for s in row]

    # def __iter__(self):
        # return self
    
#nextGroupTmpRow = []
for i in range(40):
    if i < 10:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lec\\'+str(i+229)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 20:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lec\\'+str(i+319)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 30:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lec\\'+str(i+409)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    else:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lec\\'+str(i+499)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
        
for i in range(48):
    if i < 12:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Pract\\'+str(i+217)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 2*12:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Pract\\'+str(i+315)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 3*12:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Pract\\'+str(i+403)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    else:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Pract\\'+str(i+490)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
        
for i in range(64):
    if i < 16:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lab\\'+str(i+201)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 2*16:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lab\\'+str(i+285)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    elif i < 3*16:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lab\\'+str(i+369)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
    else:
        roomw = open('D:\KPI\Kursach\Db\Rooms\Lab\\'+str(i+453)+'.csv', 'wb')
        roomWriter = UnicodeWriter(roomw, csv.excel, 'cp1251', delimiter =';')
        tabs=[]
        for i in range(60):
            tabs.append(['0'])
        roomWriter.writerows(tabs)
        roomw.close()
