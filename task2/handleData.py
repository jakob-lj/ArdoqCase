
import json
import matplotlib.pyplot as plt
import numpy as np

pInterval = 0.85

fig = plt.figure()

def getMax(data, attribute):
    m = 0
    i = -1
    for d, j in zip(data, range(len(data))):
        if d[attribute] > m:
            m = d[attribute]
            i = j
    return i, m


def getMin(data, attribute):
    m = 10e10
    i = -1
    for d, j in zip(data, range(len(data))):
        if d[attribute] < m:
            m = d[attribute]
            i = j
    return i, m

def inPInterval(element):
    pass


def calculate(region):
    result = open('data/%sGoing.json' % region, 'r')
    data = json.loads(result.read())
    result.close()

    superSum = 0
    superCounter = 0

    posMax, maxElement = getMax(data, 'avgSpeed')
    posMin, minElement = getMin(data, 'avgSpeed')

    diff = maxElement - minElement

    bottom = minElement + (1-pInterval) * diff
    top = maxElement - (1-pInterval) * diff

    y = []
    x = []
    nextX = 0

    for el, i in zip(data, range(len(data))):
        
        if bottom < el['avgSpeed'] < top:
            superSum += float(el['avgSpeed'])
            superCounter += 1
        x.append(nextX)
        y.append(el['avgSpeed'])
        nextX += 1

    tripsAvg = (superSum / superCounter)

    print("Total avarage speed in %s: %.2f m/s" % (region, tripsAvg))

    plt.title("%s-going trips, avg: %.2f" % (region, tripsAvg))
    plt.plot(x, [bottom]*len(x))
    plt.plot(x, [top]*len(x))
    plt.plot(x, y)
    plt.savefig("result/%sTrips.png" % region)
    plt.show()

calculate('west')
calculate('east')

