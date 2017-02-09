# Amy

# Cassandra

### Environment setup (on Ubuntu)
- Download Cassandra from Apache [website](http://cassandra.apache.org)
- tar -xvzf apache-cassandra-3.9-bin.tar.gz
- Modify {Cassandra Dir}/conf/cassandra.yaml, change rpc_address to 0.0.0.0, broadcast_rpc_address to localhost.
- Modify {Cassandra Dir}/conf/cassandra.yaml, change authenticator to PasswordAuthenticator
- Start Cassabdra: {Cassandra Dir}/bin/cassandra -f
- Connect Cassandra through cqlsh: cqlsh 127.0.0.1 -u cassandra -p cassandra
- In CQLSH, enter "CREATE USER your_username WITH PASSWORD 'your_password' SUPERUSER;". This will create a new super user.
- Login with new user
- In CQLSH, enter "DROP USER cassandra;"

### Create table
```
CREATE KEYSPACE mykeyspace
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
USE mykeyspace;
```

```
create table acronyms (
	acronym text,
	meaning text,
	sentence text,
	source text,
	count bigint,
    upvotes int,
    downvotes int,
	url text,
	PRIMARY KEY (acronym, meaning)
)
```

## KAFKA/Spark

### Environment setup (on Ubuntu)
- curl -O http://www.scala-lang.org/files/archive/scala-2.11.8.deb
- sudo dpkg -i scala-2.11.8.deb
- wget http://apache.claz.org/kafka/0.10.1.1/kafka_2.11-0.10.1.1.tgz
- tar -xvzf kafka_2.11-0.10.1.1.tgz
- wget http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz
- tar -xvzf spark-2.1.0-bin-hadoop2.7.tgz
- pip install kafka-python
- cd {kafka dir}
- bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic acronym
- bin/kafka-topics.sh --list --zookeeper localhost:2181

### Start Kafka
- bin/zookeeper-server-start.sh config/zookeeper.properties
- bin/kafka-server-start.sh config/server.properties

## Web service

### Environment setup (on Ubuntu)

#### Java 8 
- sudo add-apt-repository ppa:webupd8team/java
- sudo apt-get update
- sudo apt-get install oracle-java8-installer

#### PIP
- sudo apt-get install python-pip
- sudo pip install --upgrade pip

#### Flask and Flask-Restful
- sudo pip install flask
- sudo pip install flask-restful

#### Python Cassandra-driver
- sudo pip install cassandra-driver

### Start the web server
- Modify file bin/envrc with correct Cassandra parameters
- Execute bin/startWs.sh

### Test the web service
- get 
```
curl http://localhost:5000/acronyms/PDF
```
- Then you will get something like this:
```
[
    [
        "PDF",
        "Portable Document Format",
        0,
        null,
        "\"Portable Document Format\" (PDF) is a file format used to present documents in a manner independent of application software, Computer hardware or known as hardware, and operating systems.",
        "WIKIPEDIA",
        null,
        "https://en.wikipedia.org/wiki/PDF"
    ]
]
```

