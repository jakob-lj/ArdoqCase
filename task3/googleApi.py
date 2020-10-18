
import requests
from time import sleep

baseUrl = "https://maps.googleapis.com/maps/api/directions/json?mode=bicycling&origin=%s&destination=%s&key=%s"

ENABLED_FETCHING = True

def getCoordinates(point):
    return "%s,%s" % (point.lat, point.long)

def getDistance(distanceElement):
    #return distanceElement['rows'][0]['elements'][0]['distance']['value']
    try:
        return distanceElement['routes'][0]['legs'][0]['distance']['value'] # meter
    except:
        return 0
    
def fetchDistance(resultStore, trip, key, sleepTime):
    if (sleepTime > 1):
        sleep(sleepTime + 1) # qouta
    url = baseUrl % (getCoordinates(trip['start']), getCoordinates(trip['end']), key)

    if (ENABLED_FETCHING):
        result = requests.get(url)
        j = result.json()
    else:
        j = {
            'routes': [
                {
                    'legs': [
                        {
                            'distance': {
                                'value': 1000
                            }
                        }
                    ]
                }
            ]
        }
    distance = getDistance(j)
    
    t = {}
    t['avgTime'] = trip['avgTime']
    t['distance'] = distance
    t['avgSpeed'] = distance / t['avgTime']
    if (distance != 0):
        resultStore.add(t)

class TestPoint:
    def __init__(self, num = 2):
        if (num == 1):
            self.lat = 59.9136959
            self.long = 10.7502484
        else:
            self.lat = 59.910717
            self.long = 10.743066

class TestStore:
    
    def add(self, value):
        pass

if __name__ == '__main__': # used in testing
    import os
    import sys
    try:
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv('API_KEY')
    except:
        print("Missing api key... man... comon")
        sys.exit(1)

    
    start = TestPoint(1)
    end = TestPoint()

    store = TestStore()
    fetchDistance(store, {'start':start, 'end':end, 'avgTime': 100}, key)
    

