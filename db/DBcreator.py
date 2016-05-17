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
        #print data
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
    
def addinfo(tmprow, groupName):
    if not (cmp(tmprow[0], groupName)):
        flag = 0 
        groupw.seek(0)
        #prepos = 0
        linecounter = 0
        groupr.seek(0)
        sgroupReader = []
        for row in groupReader:
            sgroupReader.append(row)
        for row in sgroupReader:
            #prepos = f.tell()
            #print row[0].encode('cp1251')+' : '+tmprow[1].encode('cp1251')+', '+tmprow[2].encode('cp1251')
            #print tmprow[3].encode('cp1251')+' : '+row[1].encode('cp1251')
            if not (cmp(row[0], (tmprow[1]+':'+tmprow[2])) or cmp( tmprow[3], row[1])):
                row[2] = str(int(row[2])+1)
                sgroupReader = sorted(sgroupReader[1:],key = lambda lrow:lrow[2], reverse= True)
                roomFound=''
                if not (cmp (groupName[:2], 'ia') and cmp(groupName[:2], 'ik')): 
                    for i in range(401, 439):
                        roomFound = roomFound+str(i)+','
                    sgroupReader.insert(0, [roomFound[:-1], '', '', ''])
                elif not (cmp (groupName[:2], 'io') and cmp(groupName[:2], 'ip')): 
                    for i in range(501, 539):
                        roomFound = roomFound+str(i)+','
                    sgroupReader.insert(0, [roomFound[:-1], '', '', ''])
                elif not (cmp (groupName[:2], 'is')): 
                    for i in range(201, 239):
                        roomFound = roomFound+str(i)+','
                    sgroupReader.insert(0, [roomFound[:-1], '', '', ''])
                else:
                    for i in range(301, 339):
                        roomFound = roomFound+str(i)+','
                    sgroupReader.insert(0, [roomFound[:-1], '', '', ''])
                deleteContent(groupw)
                groupWriter.writerows(sgroupReader)
                groupw.flush()
                #print row[0].encode('cp1251')+row[2].encode('cp1251')
                flag = 1
                break
            else:
                linecounter+=1
        if not flag:
            groupw.seek(0,2)
            groupWriter.writerow([tmprow[1]+':'+tmprow[2], tmprow[3], str(1), ''])
            groupw.flush()
        return ['', '', '', ''] 
    else:
        #nextGroupTmpRow = tmprow
        return tmprow

#nextGroupTmpRow = []
fullDb = open("D:\KPI\kursach\DbPrototype1.csv", 'rb')
fullDbReader = UnicodeReader(fullDb, csv.excel, 'cp1251', delimiter = ';')
i=0
while fullDbReader:
    if not i:
        firstrow = fullDbReader.next()
    else:
        firstrow = otherrow
        #print otherrow[1].encode('cp1251')
    groupw = open('D:\KPI\Kursach\Db\Groups\\'+firstrow[0]+'.csv', 'wb')
    groupr = open('D:\KPI\Kursach\Db\Groups\\'+firstrow[0]+'.csv', 'rb')
    groupWriter = UnicodeWriter(groupw, csv.excel, 'cp1251', delimiter =';')
    groupWriter.writerow(['','','',''])

    groupReader = UnicodeReader(groupr, csv.excel, 'cp1251', delimiter = ';')
    
    """if i==1:
        addinfo(nextGroupTmpRow, row[0])        """
    otherrow = addinfo(firstrow, firstrow[0])
    try:
        while not cmp(otherrow[0], ""):
            otherrow = addinfo(fullDbReader.next(), firstrow[0])
            i=1
    except StopIteration:
        groupw.close()
        groupr.close()
        break
    groupw.close()
    groupr.close()

fullDb.close()
    
