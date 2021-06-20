import pathlib
from datetime import date as dt
from datetime import timedelta


# Each time stamp is mapped to an list of tuples in format(virtual Server address, destination Ip)
ips = dict()

# iterates through the files in current directory
for path in pathlib.Path(".").iterdir():
    # if you change the name of this file from ip.py, must change the line below or this file will be processed as well and cause errors
    if path.is_file() and path.name != 'ip.py':
        with open(path, 'r', encoding='windows-1252') as currFile:
            stamp = ''
            destination = ''
            virtualServer = ''
            for line in currFile:
                print(line)
                if 'Virtual' in line:
                    words = line.split()
                    virtualServer = words[2] 
                if 'Destination' in line:
                    words = line.split()
                    stamp = words[0][4:-5]
                    destination = words[-1]
                    if stamp in ips:
                        ips[stamp].append((virtualServer, destination))
                    else:
                        ips[stamp] = []
                        ips[stamp].append((virtualServer, destination))
        currFile.close()

skeys = ips.keys()

# converting the string time stamps to integers
keys = []
for key in skeys:
    if key:
        keys.append(int(key))
# print(keys)

# outputs dates based on those older than the input
while True:
    date = input('Enter Date in mm/dd/yy format:')
    date = date.split('/')
    stamp = int(date[2] + date[0] + date[1])
    for key in keys:
        if stamp >= key:
            print('For date ' + str(key) + ' The Idled Virtual Sever address and Destination IPs are: =========================================================================================')
            ipNd = ips[str(key)]
            for virtualServer, destination in ipNd:
                print('Virtual Server = ' + virtualServer + ' || Destination IP = ' + destination)
    date_N_days_ago = dt.today() - timedelta(days=50)
    formatt = date_N_days_ago.strftime("%m/%d/%y")
    print(formatt)
