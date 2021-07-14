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

for available_place in free_periods_in_all_places:
    print(available_place)
    # sprawdzac czy obiekt ma wolny czas dla przedzialu klienta, jak tak to wypisac nazwe obiektu

    #print(offers2)

    # ogólnie teraz trzeba byłoby dorwać się do reezerwacji jakoś i pododawać je do tych 2 słowników ??? - ogólnie nw czy to dobry nawet pomysł ale przynajmniej nie ma duplikatów
    # następnym krokiem będzie wyszukiwanie najbliższego terminu rezerwacji?

#for x in offers.find('reservations'[{}]): #{'reservations': [{}]}):
#    print(x)

#for x in offers.reservations.find():
#   print(x)
