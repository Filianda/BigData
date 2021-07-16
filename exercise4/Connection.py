from typing import FrozenSet
from pymongo import MongoClient
from datetime import date, datetime

# Connect with db
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["exercise4"]

date_time_format = "%Y-%m-%d"

# Data from user

data_from_client = datetime.strptime(input("Input arrival date (yyyy-mm-dd): "), date_time_format)
data_to_client = datetime.strptime(input("Input departure date (yyyy-mm-dd): "), date_time_format)

# collection choose
offers = db["offers"]
free_periods_in_all_places = []
for offer in offers.find():
    free_periods = []
    ready_from = datetime.strptime((offer['readyFrom']), date_time_format)
    ready_to = datetime.strptime((offer['readyTo']), date_time_format)
    reservations = offers.find_one({},{'reservations'})['reservations']

    # CHANGE STRING OF DATES TO DATETIME OBJECTS
    for reservation in reservations:
        reservation['from'] = datetime.strptime(reservation['from'], date_time_format)
        reservation['to'] = datetime.strptime(reservation['to'], date_time_format)

    # SORT RESERATIONS LIST BY FROM DATE
    reservations.sort(key=lambda reservation: reservation['from'], reverse=False)

    for reservation in reservations:
        if ready_from != reservation['from']:
            free_period = {}
            free_period['ready_from'] = ready_from
            free_period['ready_to'] = reservation['from']
            free_periods.append(free_period)

        ready_from = reservation['to']

    if ready_from != ready_to:
        free_period = {}
        free_period['ready_from'] = ready_from
        free_period['ready_to'] = ready_to
        free_periods.append(free_period)
    
    if len(free_periods) > 0:
        available_place = {}
        available_place['idObject'] = offer['idObject']
        available_place['id'] = offer['id']
        available_place['free_periods'] = free_periods
        free_periods_in_all_places.append(available_place)

print("\nFound avaliable places:")
places = db["places"]
for available_place in free_periods_in_all_places:
    for avaible_period in available_place['free_periods']:
        if data_from_client >= avaible_period['ready_from'] and data_to_client <= avaible_period['ready_to']:
            place_name = places.find_one({ "id" : available_place['idObject']})['name']
            print(place_name + " " + available_place['idObject'] + " " +  available_place['id'] + " " + avaible_period['ready_from'].strftime(date_time_format) + " " + avaible_period['ready_to'].strftime(date_time_format))
            break
