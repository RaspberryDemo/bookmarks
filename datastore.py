#!/usr/bin/python
from pymongo import *
from bson import ObjectId
from config import cas, links


def save_catalog(doc):
    find = cas.find({'name': doc['name'], 'owner': doc['owner']}).count()
    if not find:
        cas.insert(doc)


def save_links(doc):
    find = links.find({'link': doc['link'], 'name': doc['name'], 'owner': doc['owner']}).count()
    if not find:
        links.insert(doc)


def get_catalogs(owner):
    docs = cas.find({'owner': owner})
    docs = list(docs)
    return docs


def delete_catalogs(ca, owner):
    cas.remove({'name': ca, 'owner': owner})


def get_links(ca=None, owner=None):
    if not ca:
        docs = links.find({'owner': owner})
    else:
        docs = links.find({'catalog': ca, 'owner': owner})
    docs = list(docs)
    return docs


def delete_bookmark(objid=None, ca=None, owner=None):
    if objid:
        links.remove({'_id': ObjectId(objid)})
    if ca:
        links.remove({'catalog': ca, 'owner': owner})
    return
