#!/usr/bin/python
from pymongo import *
from bson import ObjectId
from flask_login import UserMixin
from config import userdb


def add_user(username, password):
    user = {'name': username, 'password': password}
    if userdb.find({'name': username}).count():
        return False
    userdb.insert(user)
    return True


def check_password(username, password):
    if userdb.find({'name': username, 'password': password}).count():
        return True
    print 'not found'
    return False


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

