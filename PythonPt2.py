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
requestsPerDay,requestsPerWeek,RequestsPerMonth=0,0,0
StartDay= 24
StartYear= 1994
StartMonth = 10
#main method
MFile = open('MarketData.txt', 'w')
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

    #If the date is not possible ie Oct 32 1994 change month
    try:
        #Checks Number of Requests per Day
        if date == datetime(StartYear, StartMonth, StartDay).date():
            requestsPerDay+=1

        else:
            #Changes Var to strings
            
            StrPerday=str(requestsPerDay)
            StrMonth=str(StartMonth)+ " "
            StrYear=str(StartYear) + ": "
            StrDay=str(StartDay) + " "

            #Changes it to the next day
            StartDay+=1

            #Writes into txt file 
            #There is probably a better way of doing this
            #Need HELP
            MFile.write(StrMonth)
            MFile.write(StrDay)
            MFile.write(StrYear)
            MFile.write(StrPerday)
            MFile.write("\n")

            requestsPerDay=1
    except:
        #If statement checks to see if its Dec
        #  means next month goes back to January next year now
        if StartMonth!= 12:
            StartMonth+=1
        else:
            StartMonth=1
            StartYear+=1
        StartDay=1
#output
print('6 months count: ', partcount, '\nTotal: ', totalcount, '\nTotal on Oct 24 1994:', requestsPerDay)
#closes files so that it can be read
MFile.close()
# Initialize a dictionary to store the counts for the first numbers.
first_number_counts = {}
instan=0
# Open the text file for reading (change 'your_file.txt' to the actual file path).
with open('MarketData.txt', 'r') as file:
    for line in file:
        # Split the line by spaces.
        parts = line.split()
        
        # Check if there is at least one part on the line.
        if parts:
            # first number is month
            # Extract the first part (the number before the first space).
            #month
            first_number = parts[0]
            #instances
            forthNum=int(parts[3])
            instan+=forthNum
            # Update the count for the first number in the dictionary.
            if first_number in first_number_counts:
                
                first_number_counts[first_number] += 1
                
            else:
                first_number_counts[first_number] = 1

# Print the counts for each first number.
for first_number, count in first_number_counts.items():
    print(f"First Number {first_number}: {count} occurrences")
print(instan)

