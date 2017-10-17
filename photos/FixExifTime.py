#!/usr/bin/python

# This program reads all the files in the current directory, parses them for the jpeg files 
# and alters the time of those files. It reads the time from the first file and
# then offsets the rest of the times by 2mins each.

#from PIL import Image
import time
import dateutil.parser
import datetime
import piexif
import imghdr

import os
import os.path

def testDate():
    # Add 5mins to current date
    d = datetime.datetime.today()
    print d

    dt = datetime.timedelta(seconds = 300)
    print d+dt

def getPicsFromCurrentDir():
    cwd = os.getcwd()

    dirEntries = os.listdir(cwd)

    files = []
    for e in dirEntries:
        if os.path.isfile(e) and imghdr.what(e) == 'jpeg':
            files.append(e)
    return files

def getFileTime(f):
    exifDict = piexif.load(f)

    datestr=""
    try: 
        datestr = exifDict["Exif"][piexif.ExifIFD.DateTimeOriginal]
    except KeyError, e:
        print 'Got KeyError' + str(e)
        print 'Using Unix modification time'
        datestr = time.ctime(os.path.getmtime(f))

    d = dateutil.parser.parse(datestr)
    return str(d)


def updateDateTimeForFile(f, time):
    exifDict = piexif.load(f)

    exifDict["Exif"][piexif.ExifIFD.DateTimeOriginal] = time

    exifBytes = piexif.dump(exifDict)
    piexif.insert(exifBytes, f)

    exifDict = piexif.load(f)
    print exifDict["Exif"]

def getTargetDateTime(time):
    d = dateutil.parser.parse(time)
    dtFiveMins = datetime.timedelta(seconds = 100)
    return str(d+dtFiveMins)

def updateDateTime(files):
    if len(files) <= 1:
        return
    targetTime = getFileTime(files[0])
    for f in files:
        print 'Updating file: ' + f
        targetTime = getTargetDateTime(targetTime)
        updateDateTimeForFile(f, targetTime)



pics = getPicsFromCurrentDir()
print pics
updateDateTime(pics) 
print 'Done!'


#testDate()
