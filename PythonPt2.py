#we talked through this process as a team, Joseph was the scribe

#import
import urllib.request as web
from datetime import datetime

#methods
def downloadFile():
    dl = web.urlopen('https://s3.amazonaws.com/tcmg476/http_access_log')
    with open('data.txt', 'wb') as file:
        file.write(dl.read())

def notSuccessful(lineIn):
    return lineIn[lineIn.index('HTTP/1.0" ')+10:lineIn.index('HTTP/1.0\" ')+11] == '3'

def redirected(lineIn):
    return lineIn[lineIn.index('HTTP/1.0" ')+10:lineIn.index('HTTP/1.0\" ')+11] == '4'
#define variables
totalcount, partcount, weekCount, notSuccessCount, redirectedCount = 0, 0, 0, 0, 0
currentMonth, currentDay = "", ""
weeksCount, dayCount = [], []

#main method

#attempt file open, download if does not already exist, the open
try:
    file = open('data.txt','r')
except:
    downloadFile()
    file = open('data.txt','r')

#add file content into individual line per http request
for line in file:
    #convert to date if it's a request (if [ and : exist in the line)
    try:
        date = datetime.strptime(line[line.index('[')+1:line.index(':')], '%d/%b/%Y').date()
    except:
        pass
    if(currentMonth != date.month):
        monthFile = open(str(date.month)+'Records', 'w')
        for i in dayCount:
            monthFile.write(currentMonth, i+1, ": ",dayCount[i], 'requests\n')
        for i in weeksCount:
            monthFile.write(currentMonth, 'Week', i+1, ": ",weeksCount[i], 'requests\n')
        monthFile.close()
    currentMonth = date.month
    currentDay = date.day
    print(currentDay)
    if(currentDay != date.day):
        dayCount.append(1)
    else:
        dayCount[currentDay-1] = dayCount[currentDay-1]+1


#output

'''
for line in file:
    try:
        if(notSuccessful(line)):
            countnotsuccess+=1
    except:
        pass
print(countnotsuccess)'''
