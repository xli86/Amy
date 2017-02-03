'''
Copy acronyms table from other cassandra db to local db
'''
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

nodeips = os.environ['CASSANDRA_CLUSTER'].split(',')
print "username=%s, password=%s" % (os.environ['CASSANDRA_USERNAME'], \
    os.environ['CASSANDRA_PASSWORD'])

cluster = Cluster(nodeips, auth_provider=PlainTextAuthProvider(\
        username=os.environ['CASSANDRA_USERNAME'], \
        password=os.environ['CASSANDRA_PASSWORD']))
cluster2 = Cluster('127.0.0.1', auth_provider=PlainTextAuthProvider(\
        username=os.environ['CASSANDRA_USERNAME'], \
        password=os.environ['CASSANDRA_PASSWORD']))
session = cluster.connect('mykeyspace')
session2 = cluster.connect('mykeyspace')
update = session2.prepare("update acronyms set upvotes=0, downvotes=0 where acronym = ? and meaning = ?")
for r in session.execute("select acronym, meaning from acronyms"):
    print r.acronym, r.meaning
    session2.execute(update, (r.acronym, r.meaning))
cluster.shutdown()
cluster2.shutdown()

