#!/usr/bin/env python
from config import apiusers


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class UsersDB(object):
    def __init__(self):
        self.admin_users_db = apiusers.admin_users_db

if __name__ == '__main__':
    print(UsersDB().admin_users_db)