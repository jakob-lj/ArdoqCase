
import json
import sys

stations = {}
uniqueTrips = 0

try:
    import time
    import datetime
    import os
    from dotenv import load_dotenv

    from googleApi import fetchDistance

    from matplotlib import pyplot as plt

    import threading
except:
    print("Did you install all necessary packages?")
    print()
    print("Create a virtual environment and run pip install -r requirements.txt")
    sys.exit(1)

OSLO_CENTRUM = {'lat':59.910717, 'long': 10.743066}

load_dotenv()

toolbar_width = 40

try:
    f = open('history.jake', 'r')
    history = json.loads(f.read())
    f.close()
except:
    history = {
        'ran':0,
        'lastRun': 0,
        'numberOfThreads':0
    }

# setup toolbar
print("Working....")
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

def getRemaingingTime(i):
    return "%i:%i" % (int(i/60), int(i%60))

class UniqueTrips:
    def __init__(self):
        self.value = 0

    def addTrip(self):
        self.value += 1

    def getUniqueTrips(self):
        return self.value

class Store:
    def __init__(self):
        self.value = []

    def add(self, value):
        self.value.append(value)

    def getAll(self):
        return self.value


class Station:
    def __init__(self, id, lat, long, name):
        self.id = id
        self.lat = lat
        self.long = long
        self.name = name
        self.trips = {}

    def __str__(self):
        return self.name

    def getDistanceToCentrum(self):
        return ((self.lat - OSLO_CENTRUM['lat']) ** 2 + (self.long - OSLO_CENTRUM['long'])**2)**(1/2)

    def isCentrum(self):
        distanceToCentrum = self.getDistanceToCentrum()
        return distanceToCentrum < 0.025
    

    def addTrip(self, station, duration, uts):
        if (station.id in self.trips.keys()):
            self.trips[station.id]['count'] += 1
            self.trips[station.id]['times'].append(duration)
        else:
            uts.addTrip()
            self.trips[station.id] = {
                'count': 1,
                'distance': 0,
                'times': [duration]
            }

    def getStation(id, lat, long, name):
        if (id in stations.keys()):
            return stations[id]
        s = Station(id, lat, long, name)
        stations[id] = s
        return s

def getDirection(start, end):
    if (start.long < end.long and end.long > OSLO_CENTRUM['long']):
        return 'EAST'
    elif (start.long > end.long and end.long < OSLO_CENTRUM['long']):
        return 'WEST'
    elif start.long < end.long and end.long < OSLO_CENTRUM['long']:
        return 'EAST'
    else:
        return 'WEST'

uniqueTripsCounter = UniqueTrips()
totalTrips = UniqueTrips()
c = 0
with open("apr19.json", "r") as f:
    d = f.read()
    j = json.loads(d)

    for trip, counter in zip(j, range(len(j))):
        hour, minute, seconds = [int(t.split(".")[0]) for t in (trip['started_at'].split()[1].split("+")[0].split(":"))]
        if ( hour == 14):
            totalTrips.addTrip()
            start = Station.getStation(trip['start_station_id'], trip['start_station_latitude'], trip['start_station_longitude'], trip['start_station_name'])
            end = Station.getStation(trip['end_station_id'], trip['end_station_latitude'], trip['end_station_longitude'], trip['end_station_name'])
            start.addTrip(end, trip['duration'], uniqueTripsCounter)
            if (counter % 600 == 0):
                sys.stdout.write("=")
                sys.stdout.flush()
        



sys.stdout.write("]\n") # this ends the progress bar
print("Finished")
print()
print("Total station length: ", end="")
print(len(stations))
print("Total unique trips:", uniqueTripsCounter.getUniqueTrips())
print("Total trips: %s"  % totalTrips.getUniqueTrips())
print("calcuated api requests cost of all unique trips: %s kr." % (uniqueTripsCounter.getUniqueTrips() / 1000 * 88))
print()
print("Calculating trips from centrum to out of centrum where at the centrum station had at least 15 differnt end stations")
print("and the trips all had more than 3 different bikes do the same trip during the time window (in avarage during the month)")

print()


print("Working....")
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
sys.stdout.write("=")
sys.stdout.write("=")

nextX = 0
tripsOfInterest = []
westGoing = []
eastGoing = []
for station, i in zip(stations, range(len(stations))):
    start = stations[station]
    numberOfTrips = len(start.trips)

    if (numberOfTrips) > 15: # only analyzing into stations where there were 15 different end stations assosiated with a trip
        for trip_key in start.trips:
            trip = start.trips[trip_key]
            start = stations[station]
            end = stations[trip_key]
            if (start.isCentrum() and not end.isCentrum()):
                if (trip['count'] > 3 or True): # only analysing trips completed more than 3 times
                    avgTime = sum(trip['times']) / trip['count']
                    direction = getDirection(start, end)
                    t = {'start': start, 'end':end, 'avgTime': avgTime}
                    if (direction == 'EAST'):
                        eastGoing.append(t)
                    else:
                        westGoing.append(t) 
                    tripsOfInterest.append(t)
        if (i % 6 == 0): 
            sys.stdout.write("=")
            sys.stdout.flush()

        nextX += 1

print()
print()
totalRequestsAfterCentrumFilter = len(westGoing) + len(eastGoing)
totalCostAfterCentrumFilter = totalRequestsAfterCentrumFilter / 1000 * 88 # calculated using todays USD currency
calculatedTotalFreeRuns = (9.1*200/totalCostAfterCentrumFilter)
print("Looking into %s number of trips" % len(tripsOfInterest))
print("calcuated api requests cost of trips for interest: %s kr." % totalCostAfterCentrumFilter)




# for trip in tripsOfInterest:
#     direction = getDirection(trip['start'], trip['end'])
#     if (direction == 'EAST'):
#         eastGoing.append(trip)
#     else:
#         westGoing.append(trip) 
#         #print("%s going trip, starts at %s and ends at %s with an avarage duration at %s" % (getDirection(trip['start'], trip['end']), trip['start'], trip['end'], trip['avgTime']))


if ( not os.getenv('API_KEY')):
    print("Cool that you got so far. However, have you considered making your own API key? You can't use mine:)")
    print()
    print("Create your api key here: https://console.cloud.google.com/apis/credentials")
    print("Remember to enable Google distancematrix API under Google Maps before creating api key under credentials")
    print("You can append your api key by runing: echo \"API_KEY=<your-api-key>\" > .env")
    sys.exit(1)
else:
    print("API KEY DETECTED. Thanks")
    print()

print("NOTE: Googles Directions API has a generous $200 free tier! You can run this program %i times inside the free tier" % (calculatedTotalFreeRuns))

print("Free tier usage: %i/%i" % (history['ran'], calculatedTotalFreeRuns))
print("Are you willing to make api calles to google the cost of %s or use one of your free runs?" % totalCostAfterCentrumFilter)
willingToPay = input(">>> (Y/N): ")

if (not willingToPay.lower() == 'y'):
    print("Ok, your loss")
    sys.exit(1)

if (history['ran'] >= int(calculatedTotalFreeRuns)):
    print("You have used up your free runs, are you actually willing to pay in order to run my crappy script??")
    willingToPay = input (">>> (Y/N): ")
    if (not willingToPay.lower() == 'y'):
        print("I get you, didn't pay for it either")
        sys.exit(1)

print("Proceeding")

eastStore = Store()
westStore = Store()
threads = []
maxSleepTime = 0

now = int(time.time()/60)
if (now - history['lastRun'] < 2): # stay inside quota if recently ran
    offset = history['numberOfThreads']
else:
    offset = 0

startedThreads = offset

for trip in eastGoing:
    sleepTime = int(startedThreads/3000)*60
    t = threading.Thread(target=fetchDistance, args=(eastStore, trip, os.getenv('API_KEY'), sleepTime)) # fetch distances in parallell
    t.start()
    threads.append(t)
    startedThreads += 1
    

for trip in westGoing:
    sleepTime = int(startedThreads/3000)*60
    maxSleepTime = sleepTime
    t = threading.Thread(target=fetchDistance, args=(westStore, trip, os.getenv('API_KEY'), sleepTime)) # fetch distances in parallell
    t.start()
    threads.append(t)
    startedThreads += 1


print("Estimated time to finish: %i seconds" % maxSleepTime)
counted = 0
while counted < maxSleepTime:
    time.sleep(1)
    print()
    sys.stdout.write("\033[F")
    #sys.stdout.write("\033[K")
    
    sys.stdout.write("Remainging sleep time in order to fulfill qouta requirements: %s min:sec" % getRemaingingTime(maxSleepTime - counted))
    sys.stdout.flush()
    counted += 1
print("Cleaing up...")
print()
for t in threads: # wait for all threads to finish
    t.join()

print("Writing results...")
print()
startedThreads = startedThreads - offset

print("Westgoing: %i, eastgoing: %s" % (len(westGoing), len(eastGoing)))
plt.title("Number of trips")
plt.bar(1, len(westGoing))
plt.bar(3, len(eastGoing))

plt.legend(['West', 'East'])
plt.savefig('result/trips.png')

print('A number of %i threads has finished' % startedThreads)
f = open('data/eastGoing.json', 'w') 
f.write(json.dumps(eastStore.getAll()))
f.close()

w = open('data/westGoing.json', 'w')
w.write(json.dumps(westStore.getAll()))
w.close()

history = {
    'ran': history['ran'] + 1,
    'lastRun': int(time.time()/60),
    'numberOfThreads': startedThreads
}

h = open('history.jake', 'w')
h.write(json.dumps(history))
h.close()