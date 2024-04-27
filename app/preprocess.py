import json
import math


def setCustomParameters(testdata, paramaterToEvaluate, parameterToGet):
    maxValue = 0
    minValue = 1000

    for car in testdata:
        if car[parameterToGet] > maxValue:
            maxValue = car[parameterToGet]
        if car[parameterToGet] < minValue:
            minValue = car[parameterToGet]

    stage = (maxValue - minValue) / 10

    for car in testdata:
        for i in range(0, 10):
            if (minValue + (i + 1) * stage - car[parameterToGet] >= 0 and minValue + (i + 1) * stage - car[parameterToGet] < stage):
                car[paramaterToEvaluate] = (i + 1)

    return testdata

def preprocessData():
    with open('db_new.json', 'r') as config_file:
        testdata = json.load(config_file)
    paramPairs = {'globalRange': 'range', 'budget': 'priceMin'}

    for paramToEvaluate in paramPairs:
        testdata = setCustomParameters(testdata, paramToEvaluate, paramPairs.get(paramToEvaluate))
        print("\n")

    testdata = setCustomParameters(testdata, 'globalRange', 'range')

    return testdata

def getCoeficient():
    print()

if __name__ == '__main__':
    preprocessedData = preprocessData()

    for car in preprocessedData:
        print(car)



