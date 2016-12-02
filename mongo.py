#!/usr/bin/python
from pymongo import *
from bson import ObjectId

ip = "192.168.0.105"


def save_catalog(doc):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    cas = db.catalogs
    find = cas.find({'name': doc['name'], 'owner': doc['owner']}).count()
    if not find:
        cas.insert(doc)


def save_links(doc):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    find = links.find({'link': doc['link'], 'name': doc['name'], 'owner': doc['owner']}).count()
    if not find:
        links.insert(doc)


def get_catalogs(owner):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    cas = db.catalogs
    docs = cas.find({'owner': owner})
    docs = list(docs)
    return docs


def delete_catalogs(ca, owner):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    cas = db.catalogs
    cas.remove({'name': ca, 'owner': owner})


def get_links(ca=None, owner=None):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    if not ca:
        docs = links.find({'owner': owner})
    else:
        docs = links.find({'catalog': ca, 'owner': owner})
    docs = list(docs)
    return docs


def delete_bookmark(objid=None, ca=None, owner=None):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    if objid:
        links.remove({'_id': ObjectId(objid)})
    if ca:
        links.remove({'catalog': ca, 'owner': owner})
    return
