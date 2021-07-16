from typing import FrozenSet
from pymongo import MongoClient
from datetime import date, datetime

# Connect with db
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["exercise4"]

date_time_format = "%Y-%m-%d"

# Data from user
yearFrom = "2020"
monthFrom = "10"
dayFrom = "23"
yearTo = "2020"
monthTo = "10"
dayTo = "23"

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
        available_place['id'] = offer['id']
        available_place['free_periods'] = free_periods
        free_periods_in_all_places.append(available_place)

data_from_client = datetime.strptime('2020-10-29',date_time_format)
data_to_client = datetime.strptime('2020-11-05',date_time_format)


for available_places in free_periods_in_all_places:
    y = (available_places['free_periods'])
    for avaible_period in available_places['free_periods']:
        if data_from_client >= avaible_period['ready_from'] and data_from_client <=  avaible_period['ready_to'] and data_to_client <= avaible_period['ready_to']:
            flag = 1 
    if flag == 1:
        print(available_places['id'])
