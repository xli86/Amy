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
cluster2 = Cluster(['127.0.0.1'], auth_provider=PlainTextAuthProvider(\
        username=os.environ['CASSANDRA_USERNAME'], \
        password=os.environ['CASSANDRA_PASSWORD']))
session = cluster.connect('mykeyspace')
session2 = cluster2.connect('mykeyspace')
insert = session2.prepare("Insert into acronyms (acronym, meaning, count, \
	upvotes, downvotes, sentence, source, url) \
	values(?, ?, 0, 0, 0, ?, ?, ?)")
i = 0
for r in session.execute("select *  from acronyms"):
    print i, r.acronym, r.meaning
    i = i+1
    session2.execute(insert, (r.acronym, r.meaning, r.sentence, r.source, r.url))
cluster.shutdown()
cluster2.shutdown()

