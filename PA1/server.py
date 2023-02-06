# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:27:57 2023

@author: zelul
"""
import os
import socket
import filetype
import argparse
import threading
from datetime import datetime

HOST = '127.0.0.1' # LOCALHOST

def msgProcess(msg,dic):
    msgList = msg.split('\r\n')
    firstLine = msgList[0].split(' ')
    method = firstLine[0]
    if firstLine[1] == '/':
        path = dic + firstLine[1]+'index.html'
    else:
        path = dic + firstLine[1]
    print(path)
    
    if method != 'GET':
        return sendResponse('403 Forbidden', 'text/html', 
        "<h1><b>HTTP 403 Forbidden</b></h1>")
    elif os.path.isfile(path):
        fy = filetype.guess(path)
        fb = open(path)
        return sendResponse('200 OK',fy.mime,fb.read())
    else:
        return sendResponse('404 Not Found', 'text/html',
        "<h1><b>HTTP 404 Not Found</b></h1>")
    

def sendResponse(status_code,contentType,content):
    response = ''
    response += "HTTP/1.0 " + status_code + '\r\n'
    response += 'Content-Type: ' + contentType + '\r\n'
    response += 'ContentLength: '+ str(len(content)) + '\r\n'
    response += 'Date: ' + str(datetime.now()) + '\r\n\r\n'
    response += content + '\r\n\r\n'
    return response


def deal(sock,addr,dic):
    print('Connected by '+ str(addr))
    try:
        data = sock.recv(1024).decode("utf-8")
        response = msgProcess(data, dic)
    except:
        response = sendResponse('400 Bad Request', 'text/html',
        "<h1><b>HTTP 400 Bad Request</b></h1>")
    sock.send(response.encode('utf-8'))
    sock.close()
    print('Loss connect with' + str(addr))
    return


def main(dic,port):
    dic = os.path.dirname(__file__) + '/' + dic
    # server_stream: TCP protocal, AF_INET: IPV4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,port))
    server.listen()
    while True:
        try:
            sock,addr = server.accept()
            xd = threading.Thread(target=deal, args=(sock,addr,dic))
            xd.start()
        except:
            print('Connection error!')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-document_root', type = str, help = 
                        'the directory which the webserver uses to server files',
                        default = './')
    parser.add_argument('-port', type = int, help = 
                        'the port that the server listens on', default= 8080)
    args = parser.parse_args()
    main(args.document_root,args.port)