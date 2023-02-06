Name: Zelu Liang

Assignment name: Distributed Systems Programming Assignment 1: Build a web server

Discription:

This is a HTTP web server which is under server/client communication architecture. There are two command line options: document root and port.

Server will keep listenning the requests from clients. Using the multithread approach to complete my web server. Once server accept a new connection, will spawn a thread to parse the request, transmit the file,etc.

index.html is the default file, so if you don't require the specific file, 'Get /' and 'Get /index.html' are the same requests.

There are four status codes available, 200 for success, 404 error is the required file doesn't exist, 403 error is the status code of request is not GET, for other situations are 400 error.


A list of submitted files:

server.py
index.html(test)
README.txt


Instructions:

command: $ python server.py -document_root "/home/moazzeni/webserver_files" -port 8888 
document_root parameter is required and must be absolute paths, 
port, the default value of port is 8080 which is not required.
The test file index.html which is the main page of scu.edu.com.


Demo/screenshots:

under screenshots/