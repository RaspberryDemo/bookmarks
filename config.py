#!/usr/bin/python
from pymongo import *

ip = '192.168.0.105'
port = 27017

cas = MongoClient(ip, port).bookmarks.catalogs
links = MongoClient(ip, port).bookmarks.links

userdb = MongoClient(ip, port).bookmarks.users
