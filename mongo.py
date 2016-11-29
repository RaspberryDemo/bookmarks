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
        print "catalog %s saved" %(doc['name'])


def save_links(doc):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    find = links.find({'link': doc['link'], 'name': doc['name'], 'owner': doc['owner']}).count()
    if not find:
        links.insert(doc)
        print "link %s saved" %(doc['name'])


def get_catalogs():
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    cas = db.catalogs
    docs = cas.find()
    docs = list(docs)
    return docs


def delete_catalogs(ca):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    cas = db.catalogs
    cas.remove({'name': ca, 'owner': ''})


def get_links(ca=None):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    if not ca:
        docs = links.find()
    else:
        docs = links.find({'catalog': ca})
    docs = list(docs)
    return docs


def delete_bookmark(objid=None, ca=None):
    client = MongoClient(ip, 27017)
    db = client.bookmarks
    links = db.links
    if objid:
        print 'link id %s' %objid
        links.remove({'_id': ObjectId(objid)})
    if ca:
        links.remove({'catalog': ca, 'owner': ''})
        print 'bookmarks belongs to %s are deleted' % ca
    return
