# Amy

# Cassandra

### Environment setup (on Ubuntu)
- Download Cassandra from Apache [website](http://cassandra.apache.org)
- tar -xvzf apache-cassandra-3.9-bin.tar.gz
- Modify {Cassandra Dir}/conf/cassandra.yaml, change rpc_address to 0.0.0.0 so that it can be accessed outside.
- Modify {Cassandra Dir}/conf/cassandra.yaml, change authenticator to PasswordAuthenticator
- Start Cassabdra: {Cassandra Dir}/bin/cassandra -f
- Connect Cassandra through cqlsh: cqlsh 127.0.0.1 -u cassandra -p cassandra
- In CQLSH, enter "CREATE USER <your_username> WITH PASSWORD '<your_password>' SUPERUSER;". This will create a new super user.
- Login with new user
- In CQLSH, enter "DROP USER cassandra;"

### Create table
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

