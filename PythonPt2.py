#we talked through this process as a team, Joseph was the scribe

#import
import urllib.request as web
import datetime
import os

#methods
def downloadFile():
    dl = web.urlopen('https://s3.amazonaws.com/tcmg476/http_access_log')
    with open('data.txt', 'wb') as file:
        file.write(dl.read())

#define variables
totalcount, partcount, dayCount, weekNum, notSuccessCount, redirectedCount = 0, 0, 0, 1, 0, 0

currentDay = datetime.date(year = 1994, month = 10, day = 24)
#main method

#attempt file open, download if does not already exist, the open
try:
    file = open('data.txt','r')
except:
    downloadFile()
    file = open('data.txt','r')

if os.path.exists("dayCount.txt"):
  os.remove("dayCount.txt")
if os.path.exists("weekCount.txt"):
  os.remove("weekCount.txt")
if os.path.exists("monthCount.txt"):
  os.remove("monthCount.txt")


#add file content into individual line per http request
for line in file:
    #convert to date if it's a request (if [ and : exist in the line)
    try:
        date = datetime.datetime.strptime(line[line.index('[')+1:line.index(':')], '%d/%b/%Y').date()
    except:
        pass
    #if date matches the specific range, add to count, add to total count regardless
    if date > datetime.datetime(1995, 6, 3).date():
        partcount+=1
    totalcount+=1
file.close()

#1) counts requests per day
while currentDay <= datetime.date(year = 1995, month = 10, day = 11):
    file = open('data.txt','r')
    dayCount = file.read().count(currentDay.strftime('%d/%b/%Y'))
    dayFile = open('dayCount.txt', 'a')
    dayFile.write(currentDay.strftime('%d/%b/%Y')+' request count: '+str(dayCount)+'\n')
    dayFile.close
    currentDay = currentDay+datetime.timedelta(days = 1)

#2.1)counts requests per week
file = open('dayCount.txt','r')
while not file.closed:
    weekCount = 0
    for i in range(7):
        if not file.closed:
            line = file.readline()
            if line != '':
                weekCount+=int(line[line.index(':')+1:line.index('\n')])
            else:
                file.close()
    weekFile = open('weekCount.txt', 'a')
    weekFile.write('Week #'+ str(weekNum) + ': '+str(weekCount)+'\n')
    weekFile.close
    weekNum += 1
file.close()

#2.2) counts requests per month
file = open('dayCount.txt','r')
currentMonth = ''
monthCount = 0
for line in file:
    if line != '':
        if line[line.index('/')+1:line.index('/')+4] == currentMonth:
            monthCount+=int(line[line.index(':')+1:line.index('\n')])
        elif currentMonth != '':
            monthFile = open('monthCount.txt', 'a')
            monthFile.write(currentMonth + ': '+str(monthCount)+'\n')
            monthFile.close
            monthCount = 0
            currentMonth = line[line.index('/')+1:line.index('/')+4]
        else:
            currentMonth = line[line.index('/')+1:line.index('/')+4]
file.close()
#3 percentage of unsuccessful requests
def notSuccessful(lineIn):
    return lineIn[lineIn.index('HTTP/1.0" ')+10:lineIn.index('HTTP/1.0\" ')+11] == '3'
file = open('data.txt', 'r')
countnotsuccess = 0
for line in file:
    try:
        if(notSuccessful(line)):
            countnotsuccess+=1
    except:
        pass
print(countnotsuccess/totalcount *100, '%')
file.close()

#4 percentage of redirected requests
def redirected(lineIn):
    return lineIn[lineIn.index('HTTP/1.0" ')+10:lineIn.index('HTTP/1.0\" ')+11] == '4'
file = open('data.txt', 'r')
countredirect = 0
for line in file:
    try:
        if(redirected(line)):
            countredirect+=1
    except:
        pass
print(countredirect/totalcount * 100, '%')
file.close()

#5 most requested 
requestedfiles = {}
for line in open('data.txt', 'r'):
    try:
        filename = line[line.index("GET ")+4:line.index('HTTP/1.0')]
        if filename in requestedfiles:
            requestedfiles[filename]+=1
        else:
            requestedfiles[filename] = 1
    except:
        pass
max = 0
maxfilename = ''
for i in requestedfiles:
    if requestedfiles[i] > max:
        max = requestedfiles.get(i)
        maxfilename = i
print(maxfilename, max)


min = 200
minfilename = ''
for i in requestedfiles:
    if requestedfiles[i] < min:
        min= requestedfiles.get(i)
        minfilename = i
print(minfilename, min)

#break up data.txt into separate files
file = open('data.txt', 'r')
for line in file:
    try:
        date = datetime.datetime.strptime(line[line.index('[')+1:line.index(':')], '%d/%b/%Y').date()
        monthLogFile = open(str(line[line.index('[')+4:line.index('[')+7])+'Log.txt', 'a')
        monthLogFile.write(line)
    except:
        pass
file.close()