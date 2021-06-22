import pathlib
from datetime import date as dt
from datetime import timedelta


# Each time stamp is mapped to an list of tuples in format(virtual Server address, destination Ip)
ips = dict()
index = 0
pathnames = set()
for path in pathlib.Path(".").iterdir():
    # if you change the name of this file from ip.py, must change the line below or this file will be processed as well and cause errors
    if path.name != '.DS_Store' and path.name != 'ip.py':
        with open(path, 'r', encoding='windows-1252') as currFile:
            stamp = ''
            destination = ''
            virtualServer = ''
            for line in currFile:
                # print(line)
                if 'Status' in line and 'STANDBY' in line:
                    break
                if 'Virtual' in line:
                    words = line.split()
                    virtualServer = words[2] 
                if 'Destination' in line:
                    words = line.split()
                    destination = words[-1]
                if 'Bits Out' in line:
                    words = line.split()
                    stamp = words[0][4:-5]
                    if stamp in ips:
                        ips[stamp].append((virtualServer, destination, path.name))
                    else:
                        ips[stamp] = []
                        ips[stamp].append((virtualServer, destination, path.name))
                    pathnames.add(path.name)
                
        currFile.close()
    index += 1

skeys = ips.keys()

# converting the string time stamps to integers
keys = []
for key in skeys:
    if key:
        keys.append(int(key))


pathnames = list(pathnames)
pathnames.sort()
print("The active load balancers are:")
print('00. All')
allLoadBalancers = []
for i in range(len(pathnames)):
    print(str(i) + '. ' + pathnames[i][0:10])
    allLoadBalancers.append(i)
numbers = input("Enter numbers of the files to analyze, seperated by spaces:")
numbers = numbers.split(' ')
chosen = []
if numbers[0] == '00':
    chosen = allLoadBalancers
else:
    for number in numbers:
        chosen.append(int(number))

keys.sort()
# outputs dates based on those older than the input
while True:
    n = input('Enter Minimum time Idled for servers (in days):')
    n = int(n)
    date_N_days_ago = dt.today() - timedelta(days=n)
    date = date_N_days_ago.strftime("%m/%d/%y")
    date = date.split('/')
    stamp = int(date[2] + date[0] + date[1])
    for key in keys:
        for number in chosen:   
            if stamp >= key:
                # print('For date ' + str(key) + ' The Idled Virtual Sever address and Destination IPs are: =========================================================================================')
                ipNd = ips[str(key)]
                for virtualServer, destination, filename in ipNd:
                    if filename == pathnames[number]:
                        stampDays = str(key)
                        stampDays = dt(int('20' + stampDays[0:2]), int(stampDays[2:4]), int(stampDays[4:]))
                        days = dt.today() - stampDays
                        # print(days)
                        days = str(days).split(' ')
                        days = days[0]
                        print('File Names = ' + filename + ' || Idle Days = ' + str(days) +  ' || Virtual Server = ' + virtualServer + ' || Destination IP = ' + destination)