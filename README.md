# Amy

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

