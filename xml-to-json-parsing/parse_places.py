import xml.etree.ElementTree as ET
from pymongo import MongoClient

tree = ET.parse('places.xml')
print("XML file loaded successfully")

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["exercise4"]
placesCollection = db["places"]


placesNode = tree.getroot()
places = []
for place in placesNode:
    placesCollection.insert_one({
        "id": place.attrib["id"],
        "name": place.text
    })
