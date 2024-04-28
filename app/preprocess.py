import json
import math
from itertools import islice

NORMALIZER = 1000000

configurationTest = {
    "name": "Mercedes",
    "horsepower": 200,
    "priceMin": 50000,
    "priceMax": 75000,
    "consumption": 15,
    "range": 300,
    "rangeIn": 500,
    "seats": 4,
    "chargeTime": 45,
    "is4Matic": False,
    "size": 3,
    "globalRange": 7,
    "budget": 50000
}
weightsTest = {
    "horsepower": 2,
    "priceMin": 9,
    "priceMax": 8,
    "consumption": 10,
    "range": 3,
    "rangeIn": 7,
    "seats": 10,
    "chargeTime": 4,
    "is4Matic": 9,
    "size": 8,
    "globalRange": 1,
    "budget": 2
}


def normalize(testdata, configuration, parameterToNormalize):
    maxValue = 0.001
    minValue = 1000

    old_data = testdata

    for car in testdata:
        if car[parameterToNormalize] > maxValue:
            maxValue = car[parameterToNormalize]
        if car[parameterToNormalize] < minValue:
            minValue = car[parameterToNormalize]

    if parameterToNormalize != 'is4Matic':
        configuration[parameterToNormalize] = configuration[parameterToNormalize] = (1 + (9 / (maxValue - minValue))
                                                                                     * (configuration[
                                                                                            parameterToNormalize] - minValue))

    for car in testdata:
        if parameterToNormalize == 'budget':
            car[parameterToNormalize] = 1 + (9 / (maxValue - minValue)) * (car['priceMin'] - minValue)
        else:
            car[parameterToNormalize] = 1 + (9 / (maxValue - minValue)) * (car[parameterToNormalize] - minValue)

    return testdata, configuration


# def preprocessData():
#     with open('db_new.json', 'r') as config_file:
#         testdata = json.load(config_file)
#     paramPairs = {'globalRange': 'range', 'budget': 'priceMin'}
#
#     for paramToEvaluate in paramPairs:
#         testdata = setCustomParameters(testdata, paramToEvaluate, paramPairs.get(paramToEvaluate))
#         print("\n")
#
#     testdata = setCustomParameters(testdata, 'globalRange', 'range')
#
#     return testdata


def matchCars(preprocessedData, weights, configuration):
    final_dictionary = {}
    propertiesToProcess = {"horsepower", "consumption", "chargeTime", "range", "budget"}
    configuration['budget'] = (configuration['priceMin'] + configuration['priceMax']) / 2

    for prop in propertiesToProcess:
        res = normalize(preprocessedData, configuration, prop)
        preprocessedData = res[0]
        configuration = res[1]

    for car in preprocessedData:
        deviation = 0
        for prop in propertiesToProcess:
            deviation += weights[prop] * abs(configuration[prop] - car[prop]) / NORMALIZER
        final_dictionary.update({deviation: car})

    ranked_dict = dict(sorted(final_dictionary.items()))

    result_str = 'I have found following cars for you: \n'
    for i in range(0, 3):
        suggested_car = ranked_dict[list(ranked_dict.keys())[i]]
        car = None

        with open('db_new.json', 'r') as config_file:
            old_data = json.load(config_file)
        for entry in old_data:
            if entry['name'] == suggested_car.get('name'):
                car = entry
                break

        suggestion = (car.get("name") + ", starting from " + str(car.get("priceMin")) + " EUR, "
                      + str(car.get("horsepower")) + " HP, " + str(car.get("consumption")) + " W/100km, "
                      + str(car.get("range")) + " km range" + '\n')
        result_str += suggestion

    return result_str


def get_matching_names(model_name):
    with open('db_new.json', 'r') as config_file:
        data = json.load(config_file)

    possible_names = []
    for entry in data:
        if model_name in entry['name']:
            possible_names.append(entry['name'])

    return possible_names


if __name__ == '__main__':
    with open('db_new.json', 'r') as config_file:
        testdata = json.load(config_file)
    print(matchCars(testdata, weightsTest, configurationTest))
