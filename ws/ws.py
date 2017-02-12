'''
ws.py
webservice
'''
import os
import json
import redis

from flask import Flask
from flask import redirect
from flask_restful import reqparse, abort, Api, Resource

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory

from kafka import KafkaProducer


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('acronym', trim=True)
parser.add_argument('meaning', trim=True)
parser.add_argument('type', choices=['up', 'down'], \
    case_sensitive=False, trim=True)

#print "username=%s, password=%s" % (os.environ['CASSANDRA_USERNAME'], os.environ['CASSANDRA_PASSWORD'])
cluster = Cluster(os.environ['CASSANDRA_CLUSTER'].split(','),\
        auth_provider=PlainTextAuthProvider(\
        username=os.environ['CASSANDRA_USERNAME'], \
        password=os.environ['CASSANDRA_PASSWORD']))
session = cluster.connect('mykeyspace')
session.row_factory = dict_factory

producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVERS'].split(','))

cache = redis.StrictRedis(host=os.environ['REDIS_HOST'],\
         port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])

@app.route('/')
def index():
    return redirect('/static/index.html')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def query_db(acronym):
    return list(session.execute(\
        "select * from acronyms where acronym='%s'" % acronym))

def query(acronym, meaning):
    for r in ACRONYMS[acronym]:
        if r['meaning'] == meaning:
            return r

def abort_if_empty(r):
    if r is None or len(r) == 0:
        abort(404, message="doesn't exist")

# acronym
# shows a single acronym item
class Acronyms(Resource):

    def get(self, acronym):
        r = query_db(acronym)
        abort_if_empty(r)
        try:
            producer.send('acronyms', acronym.encode('utf-8'))
        except Exception as e:
            print "send %s to Kafka failed" % acronym
            print e.message
        return r, 200

    def options (self):
        return {'Allow' : 'GET' }, 200, \
            { 'Access-Control-Allow-Methods' : 'GET'}

# stats
# shows a single stat
class Stats(Resource):

    def get(self, key):
        r = []
        try:
            r = json.loads(cache.get(key))
        except Exception as e:
            print "get %s from redis failed" % key
            print e.message
        return r, 200

    def options (self):
        return {'Allow' : 'GET' }, 200, \
            { 'Access-Control-Allow-Methods' : 'GET'}

## Actually setup the Api resource routing here
api.add_resource(Acronyms, '/acronyms/<acronym>')
api.add_resource(Stats, '/stats/<key>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
