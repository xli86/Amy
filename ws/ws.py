'''
ws.py
webservice, use
'''
import os
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

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

'''
@app.teardown_appcontext
def teardown_db(exception):
    if session is not None:
        session.shutdown()
    if cluster is not None:
        cluster.shutdown()
    print 'cluster shutdown'
'''

def query_db(acronym):
    return list(session.execute(\
        "select * from acronyms where acronym='%s'" % acronym))

def query(acronym, meaning):
    for r in ACRONYMS[acronym]:
        if r['meaning'] == meaning:
            return r

def upvote(acronym, meaning):
    r = query(acronym, meaning)
    if r is not None:
        r['count'] = r['count'] + 1
    return r

def downvote(acronym, meaning):
    r = query(acronym, meaning)
    if (r is not None) and (r['count'] > 0):
        r['count'] = r['count'] - 1
    return r


def abort_if_empty(r):
    if r is None or len(r) == 0:
        abort(404, message="doesn't exist")

# acronym
# shows a single acronym item and lets you delete a acronym item
class Acronyms(Resource):

    def get(self, acronym):
        r = query_db(acronym)
        abort_if_empty(r)
        return r

# UpVotes
class UpVotes(Resource):

    def get(self, acronym, meaning):
        return query(acronym, meaning)

    def put(self, acronym, meaning):
        abort_if_acronym_doesnt_exist(acronym, meaning)
        upvote(acronym, meaning)
        return query(acronym, meaning)

    def delete(self, acronym, meaning):
        abort_if_acronym_doesnt_exist(acronym, meaning)
        downvote(acronym, meaning)
        return query(acronym, meaning)

# UpVotes
class DownVotes(Resource):

    def get(self, acronym, meaning):
        return query(acronym, meaning)

    def put(self, acronym, meaning):
        abort_if_acronym_doesnt_exist(acronym, meaning)
        downvote(acronym, meaning)
        return query(acronym, meaning), 201

    def delete(self, acronym, meaning):
        abort_if_acronym_doesnt_exist(acronym, meaning)
        upvote(acronym, meaning)
        return query(acronym, meaning), 204

##
## Actually setup the Api resource routing here
##
api.add_resource(Acronyms, '/acronyms/<acronym>')
api.add_resource(UpVotes, '/<acronym>/<meaning>/votes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
