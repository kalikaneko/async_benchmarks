import random
import string

import couchdb

DB_NAME = 'couch-benchmarks'

def get_random_payload():
    return ''.join((random.choice(string.ascii_lowercase) for x in xrange(1000)))

def get_db():
    couch = couchdb.Server()
    try:
        db = couch.create(DB_NAME)
    except:
        couch.delete(DB_NAME)
        db = couch.create(DB_NAME)
    return db

def delete_db():
    couch = couchdb.Server()
    couch.delete(DB_NAME)
