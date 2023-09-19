#we talked through this process as a team, Joseph was the scribe

#import
import urllib.request as web
from datetime import datetime

#methods
def downloadFile():
    dl = web.urlopen('https://s3.amazonaws.com/tcmg476/http_access_log')
    with open('data.txt', 'wb') as file:
        file.write(dl.read())

#define variables
totalcount, partcount = 0, 0

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
    #if date matches the specific range, add to count, add to total count regardless
    if date > datetime(1995, 6, 3).date():
        partcount+=1
    totalcount+=1
#output
print('6 months count: ', partcount, '\nTotal: ', totalcount)
