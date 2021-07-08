import xml.etree.ElementTree as ET
from pymongo import MongoClient

tree = ET.parse('offers.xml')
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["exercise4"]
offersCollection = db["offers"]

offersNode = tree.getroot()
offers = []
for offer in offersNode:
    reservationsNode = offer.find("reservations")
    reservations = []
    for reservation in reservationsNode:
        reservations.append({
            "from": reservation.attrib["from"],
            "to": reservation.attrib["to"]
        })
    offersCollection.insert_one({
        "idObject": offer.attrib["idObject"],
        "id": offer.attrib["id"],
        "name": offer.find("name").text,
        "readyFrom": offer.find("readyFrom").text,
        "readyTo": offer.find("readyTo").text,
        "reservations": reservations
    })
