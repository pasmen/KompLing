from Mention.Person import Persona
from Mention.Attraction import Attractions
import pymongo
import re
from Mention.WordVec import *

def ReadDataBase(database):
    lst = []
    for i in database.find():
        lst.append(i['text'].strip())
    return lst


def PostOffers(lst_offers):
    offers = []
    for i in lst_offers:
        i = i.split('.')
        for j in i:
            offers.append(j.strip())
    return offers


def ObtainPerson(mention, offers):
    Obtain_mention_offers = set()
    for i in mention.keys():
        i = set(i.lower().split(' ') + [mention[i].lower()])
        for j in offers:
            text = set(list(filter(None, re.split('\W', j.lower()))))
            if len(i & text) > 0:
                Obtain_mention_offers.add(j)
    return Obtain_mention_offers


def ObtainAttraction(mention, offers):
    Obtain_mention_offers = set()
    for i in mention:
        i = set(i.split(' '))
        for j in offers:
            text = set(list(filter(None, re.split('\W', j.lower()))))
            if len(i & text) > 0:
                Obtain_mention_offers.add(j)
    return Obtain_mention_offers


person = Persona('Files\\Person\\persona.txt')
attraction = Attractions('Files\\Attraction\\attractions.txt')

person.ReadFileText()
attraction.ReadFileText()

person.ListPersonPosition()
attraction.ListAttractions()

person.DictFIOPosition()
attraction.SetAttractions()

person.PostProcessing()

# mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
client = pymongo.MongoClient("localhost", 27017)

db = client['datasite']
collection = db['sitereview']

lst_text = ReadDataBase(collection)

post_offers = PostOffers(lst_text)

mentions_person = ObtainPerson(person.dct_person_position, post_offers)
mentions_attraction = ObtainAttraction(attraction.set_attractions, post_offers)

database = client['Mention']
mention = database.mention

mention.delete_many({})

person = '.'.join(mentions_person) if len(mentions_person) else ''
attraction = '.'.join(mentions_attraction) if len(mentions_attraction) > 0 else ''

Mention = {'Person': person, 'Attraction': attraction}

mention.insert(Mention)

WordModel(person + attraction)